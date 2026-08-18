#!/usr/bin/env bash
set -euo pipefail

usage() {
    cat <<EOF
Usage: $(basename "$0") [options]

Options:
  -o, --output DIR    Output directory for build artifacts (default: bin)
  -c, --config PATH   Build config: debug | release (default: release)
  -t, --target OS/ARCH  Override target platform (e.g. linux/amd64)
  -ldflags FLAGS      Extra -ldflags appended to the release defaults
  -tags TAGLIST       Extra build tags passed to go build
  -h, --help          Show this help message
EOF
}

output_dir="bin"
build_config="release"
target=""
extra_ldflags=""
tags=""
entrypoint="cmd/gamemerge"
binary_name="gamemerge"

while [[ $# -gt 0 ]]; do
    case "$1" in
        -o|--output)
            [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 1; }
            output_dir="$2"
            shift 2
            ;;
        -c|--config)
            [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 1; }
            build_config="$2"
            shift 2
            ;;
        -t|--target)
            [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 1; }
            target="$2"
            shift 2
            ;;
        -ldflags)
            [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 1; }
            extra_ldflags="$2"
            shift 2
            ;;
        -tags)
            [[ $# -ge 2 ]] || { echo "missing value for $1" >&2; exit 1; }
            tags="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

if ! command -v go >/dev/null 2>&1; then
    echo "go toolchain not found in PATH" >&2
    exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/.." && pwd)"

if [[ ! -f "${repo_root}/go.mod" ]]; then
    echo "go.mod not found at ${repo_root}" >&2
    exit 1
fi

cd "$repo_root"

mkdir -p "$output_dir"
output_dir="$(cd "$output_dir" && pwd)"

go_version="$(go version | awk '{print $3}')"
commit="$(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
build_time="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

base_ldflags=(
    "-s"
    "-w"
    "-X main.version=${commit}"
    "-X main.buildTime=${build_time}"
    "-X main.goVersion=${go_version}"
)

goos="$(go env GOOS)"
goarch="$(go env GOARCH)"

if [[ -n "$target" ]]; then
    target_os="${target%/*}"
    target_arch="${target#*/}"
    if [[ -z "$target_os" || -z "$target_arch" || "$target_os" == "$target" ]]; then
        echo "invalid target '$target', expected OS/ARCH (e.g. linux/amd64)" >&2
        exit 1
    fi
    goos="$target_os"
    goarch="$target_arch"
fi

binary_path="${output_dir}/${binary_name}-${goos}-${goarch}"

case "$build_config" in
    release)
        ;;
    debug)
        base_ldflags=()
        ;;
    *)
        echo "invalid build config: $build_config (expected debug or release)" >&2
        exit 1
        ;;
esac

if [[ ${#base_ldflags[@]} -gt 0 ]]; then
    ldflags_args=(-ldflags "$(IFS=' '; echo "${base_ldflags[*]} ${extra_ldflags}")")
else
    ldflags_args=()
fi

tags_args=()
if [[ -n "$tags" ]]; then
    tags_args=(-tags "$tags")
fi

echo ">> go mod download"
go mod download

echo ">> go mod tidy"
go mod tidy

echo ">> GOOS=${goos} GOARCH=${goarch} go build -trimpath ${ldflags_args[*]:-} ${tags_args[*]:-} -o ${binary_path} ./${entrypoint}"
GOOS="$goos" GOARCH="$goarch" go build -trimpath "${ldflags_args[@]}" "${tags_args[@]}" -o "$binary_path" "./${entrypoint}"

echo ">> build complete: $binary_path"