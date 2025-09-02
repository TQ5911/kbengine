SCRIPT_HOTRELOAD = "../scripts/server_common/hotReload.py"
def main():
    gen_script_list = []
    with open(SCRIPT_HOTRELOAD, encoding="utf-8") as fr:
        for line in fr:
            if not line.strip():
                continue

            gen_script_list.append(line)

    gen_script_list.extend([
        "if KBEngine.component == 'cellapp':\n"
        "    refreshCell()\n",
        "else:\n",
        "    refreshBase()\n",
    ])

    final_str = ''.join(gen_script_list)

    with open("temp.py", "w", encoding="utf-8") as fw:
        fw.write(final_str)

    with open("hotReloadTemp.py", "r", encoding="utf-8") as fr:
        data = fr.read()
        with open(SCRIPT_HOTRELOAD, "w", encoding="utf-8") as fw:
            fw.write(data)


if __name__ == "__main__":
    main()
