package mysql

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

type Config struct {
	Host     string
	Port     int
	Username string
	Password string
	DB       string
}

func (c Config) DSN() string {
	return fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?parseTime=true&charset=utf8mb4&loc=Local&interpolateParams=true",
		c.Username, c.Password, c.Host, c.Port, c.DB)
}

func Open(cfg Config) (*sql.DB, error) {
	db, err := sql.Open("mysql", cfg.DSN())
	if err != nil {
		return nil, fmt.Errorf("open mysql: %w", err)
	}
	db.SetConnMaxLifetime(time.Minute)
	// 调大到 32/16 以支撑 Job.Run 的层级并发（Layer 0 一次 ~7 个 Pipeline 同时
	// 跑，每个 Pipeline 占 src reader + dst writer 各 1 个连接 + 启动时 SHOW COLUMNS
	// 等瞬时占用）。src 和 dst 是两个独立 *sql.DB，各自有自己的池。
	db.SetMaxOpenConns(32)
	db.SetMaxIdleConns(16)
	return db, nil
}

func Ping(ctx context.Context, db *sql.DB) error {
	ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
	defer cancel()
	return db.PingContext(ctx)
}

func Columns(ctx context.Context, db *sql.DB, table string) ([]string, error) {
	infos, err := ColumnsEx(ctx, db, table)
	if err != nil {
		return nil, err
	}
	names := make([]string, len(infos))
	for i, c := range infos {
		names[i] = c.Name
	}
	return names, nil
}

type ColumnInfo struct {
	Name     string
	Type     string
	Null     string
	Key      string
	Default  sql.NullString
	Extra    string
	AutoIncr bool
}

func ColumnsEx(ctx context.Context, db *sql.DB, table string) ([]ColumnInfo, error) {
	rows, err := db.QueryContext(ctx, fmt.Sprintf("SHOW COLUMNS FROM `%s`", table))
	if err != nil {
		return nil, fmt.Errorf("show columns %s: %w", table, err)
	}
	defer rows.Close()

	var out []ColumnInfo
	for rows.Next() {
		var (
			col   string
			ctype string
			null  string
			key   string
			def   sql.NullString
			extra string
		)
		if err := rows.Scan(&col, &ctype, &null, &key, &def, &extra); err != nil {
			return nil, fmt.Errorf("scan column: %w", err)
		}
		out = append(out, ColumnInfo{
			Name:     col,
			Type:     ctype,
			Null:     null,
			Key:      key,
			Default:  def,
			Extra:    extra,
			AutoIncr: strings.Contains(strings.ToLower(extra), "auto_increment"),
		})
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate columns: %w", err)
	}
	return out, nil
}

// WriteColumns 返回写入 dst 时应包含的全部列名（含 auto_increment）。
//
// auto_increment 列保留：合服流程通常希望显式写入按 base 偏移后的 id，
// 让 MySQL 接受这个具体值；如果不想写入某列，由 caller 自己用 colIdxs 跳过。
func WriteColumns(infos []ColumnInfo) []string {
	out := make([]string, 0, len(infos))
	for _, c := range infos {
		out = append(out, c.Name)
	}
	return out
}

// PrimaryKeyColumn 返回表的主键列名（单列主键）。复合主键直接报 error：
// 合服阶段的 CursorSource 是单列游标扫描，对复合 PK 会丢/重行。
func PrimaryKeyColumn(ctx context.Context, db *sql.DB, table string) (string, error) {
	cols, err := ColumnsEx(ctx, db, table)
	if err != nil {
		return "", fmt.Errorf("primary key %s: %w", table, err)
	}
	var pk string
	for _, c := range cols {
		if c.Key != "PRI" {
			continue
		}
		if pk != "" {
			return "", fmt.Errorf("primary key %s: composite primary key not supported (have %q, %q)", table, pk, c.Name)
		}
		pk = c.Name
	}
	if pk == "" {
		return "", fmt.Errorf("primary key %s: no primary key column found", table)
	}
	return pk, nil
}