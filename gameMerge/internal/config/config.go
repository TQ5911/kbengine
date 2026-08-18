package config

import (
	"bytes"
	"fmt"
	"io"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Databases map[string]MySQL `yaml:"databases"`
	Merge     Merge            `yaml:"merge"`
}

type MySQL struct {
	Host     string `yaml:"host"`
	Port     int    `yaml:"port"`
	Username string `yaml:"username"`
	Password string `yaml:"password"`
	DB       string `yaml:"db"`
	ServerID int    `yaml:"server_id"`
}

type Merge struct {
	Jobs       []ServerPair `yaml:"jobs"`
	Root       string       `yaml:"root"`
	ReadBatch  int          `yaml:"read_batch"`
	WriteBatch int          `yaml:"write_batch"`
}

type ServerPair struct {
	Src string `yaml:"src"`
	Dst string `yaml:"dst"`
}

type ResolvedJob struct {
	SrcConfig MySQL
	DstConfig MySQL
	SrcName   string
	DstName   string
}

func (c *Config) Resolve(p ServerPair) (*ResolvedJob, error) {
	src, ok := c.Databases[p.Src]
	if !ok {
		return nil, fmt.Errorf("databases has no entry named %q (referenced as src)", p.Src)
	}
	dst, ok := c.Databases[p.Dst]
	if !ok {
		return nil, fmt.Errorf("databases has no entry named %q (referenced as dst)", p.Dst)
	}
	return &ResolvedJob{
		SrcConfig: src,
		DstConfig: dst,
		SrcName:   p.Src,
		DstName:   p.Dst,
	}, nil
}

func Load(path string) (*Config, error) {
	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("read config %q: %w", path, err)
	}

	decoder := yaml.NewDecoder(bytes.NewReader(data))
	decoder.KnownFields(true)

	var cfg Config
	if err := decoder.Decode(&cfg); err != nil {
		return nil, fmt.Errorf("decode config %q: %w", path, err)
	}

	var extra any
	if err := decoder.Decode(&extra); err != io.EOF {
		if err != nil {
			return nil, fmt.Errorf("decode config %q: %w", path, err)
		}
		return nil, fmt.Errorf("decode config %q: multiple YAML documents are not allowed", path)
	}

	cfg.Merge.applyDefaults()
	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("validate config %q: %w", path, err)
	}

	return &cfg, nil
}

func (c Config) Validate() error {
	if len(c.Databases) == 0 {
		return fmt.Errorf("databases must contain at least one entry")
	}
	for name, db := range c.Databases {
		if err := db.validate(name); err != nil {
			return err
		}
	}
	if len(c.Merge.Jobs) == 0 {
		return fmt.Errorf("merge.jobs must contain at least one entry")
	}
	for i, job := range c.Merge.Jobs {
		if strings.TrimSpace(job.Src) == "" {
			return fmt.Errorf("merge.jobs[%d].src is required", i)
		}
		if strings.TrimSpace(job.Dst) == "" {
			return fmt.Errorf("merge.jobs[%d].dst is required", i)
		}
		if job.Src == job.Dst {
			return fmt.Errorf("merge.jobs[%d]: src and dst cannot be the same (%q)", i, job.Src)
		}
		if _, ok := c.Databases[job.Src]; !ok {
			return fmt.Errorf("merge.jobs[%d].src references unknown database %q", i, job.Src)
		}
		if _, ok := c.Databases[job.Dst]; !ok {
			return fmt.Errorf("merge.jobs[%d].dst references unknown database %q", i, job.Dst)
		}
	}
	return nil
}

func (m *Merge) applyDefaults() {
	if strings.TrimSpace(m.Root) == "" {
		m.Root = "Avatar"
	}
	if m.ReadBatch <= 0 {
		m.ReadBatch = 1000
	}
	if m.WriteBatch <= 0 {
		m.WriteBatch = 400
	}
}

func (c MySQL) validate(name string) error {
	if strings.TrimSpace(c.Host) == "" {
		return fmt.Errorf("%s.host is required", name)
	}
	if c.Port < 1 || c.Port > 65535 {
		return fmt.Errorf("%s.port must be between 1 and 65535", name)
	}
	if strings.TrimSpace(c.Username) == "" {
		return fmt.Errorf("%s.username is required", name)
	}
	if strings.TrimSpace(c.DB) == "" {
		return fmt.Errorf("%s.db is required", name)
	}
	return nil
}