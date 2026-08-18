package merger

import (
	"database/sql"
)

func NullInt64(v int64) sql.NullInt64 {
	return sql.NullInt64{Int64: v, Valid: true}
}

func NullInt64Ptr(v *int64) sql.NullInt64 {
	if v == nil {
		return sql.NullInt64{}
	}
	return sql.NullInt64{Int64: *v, Valid: true}
}

func NullString(s string) sql.NullString {
	if s == "" {
		return sql.NullString{}
	}
	return sql.NullString{String: s, Valid: true}
}

func NullBytes(b []byte) []byte {
	if b == nil {
		return []byte{}
	}
	return b
}