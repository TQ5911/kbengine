package merger

import (
	"context"
	"database/sql"
	"fmt"
)

type CursorSource struct {
	Meta_  TableMeta
	DB     *sql.DB
	Table  string
	IDCol  string
	Batch  int
	curVal any
	first  bool
}

func NewCursorSource(db *sql.DB, table, idCol string, columns []string, batch int) *CursorSource {
	if batch <= 0 {
		batch = 1000
	}
	return &CursorSource{
		Meta_: NewTableMeta(table, columns),
		DB:    db,
		Table: table,
		IDCol: idCol,
		Batch: batch,
		first: true,
	}
}

func (s *CursorSource) Meta() TableMeta { return s.Meta_ }

func (s *CursorSource) Next(ctx context.Context) ([]Row, error) {
	var (
		rows *sql.Rows
		err  error
	)
	if s.first {
		rows, err = s.DB.QueryContext(ctx, fmt.Sprintf(
			"SELECT %s FROM `%s` ORDER BY `%s` LIMIT %d",
			s.joinCols(), s.Table, s.IDCol, s.Batch))
		s.first = false
	} else {
		rows, err = s.DB.QueryContext(ctx, fmt.Sprintf(
			"SELECT %s FROM `%s` WHERE `%s` > ? ORDER BY `%s` LIMIT %d",
			s.joinCols(), s.Table, s.IDCol, s.IDCol, s.Batch), s.curVal)
	}
	if err != nil {
		return nil, fmt.Errorf("query %s: %w", s.Table, err)
	}
	defer rows.Close()

	out := make([]Row, 0, s.Batch)
	for rows.Next() {
		row := make(Row, len(s.Meta_.Columns))
		dests := make([]any, len(row))
		for i := range dests {
			dests[i] = &row[i]
		}
		if err := rows.Scan(dests...); err != nil {
			return nil, fmt.Errorf("scan %s: %w", s.Table, err)
		}
		out = append(out, row)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate %s: %w", s.Table, err)
	}
	if len(out) == 0 {
		return nil, ErrSourceDone
	}
	last := out[len(out)-1]
	v, ok := s.Meta_.Get(last, s.IDCol)
	if !ok {
		return nil, fmt.Errorf("cursor: missing id column %s", s.IDCol)
	}
	s.curVal = v
	return out, nil
}

func (s *CursorSource) joinCols() string {
	out := make([]string, 0, len(s.Meta_.Columns))
	for _, c := range s.Meta_.Columns {
		out = append(out, "`"+c+"`")
	}
	out2 := ""
	for i, c := range out {
		if i > 0 {
			out2 += ", "
		}
		out2 += c
	}
	return out2
}

type BulkSink struct {
	DB      *sql.DB
	Table   string
	Batch   int
	buf     []any
	cols    []string
	colIdxs []int
}

func NewBulkSink(db *sql.DB, table string, columns []string, colIdxs []int, batch int) *BulkSink {
	if batch <= 0 {
		batch = 400
	}
	if colIdxs == nil {
		colIdxs = make([]int, len(columns))
		for i := range colIdxs {
			colIdxs[i] = i
		}
	}
	return &BulkSink{
		DB:      db,
		Table:   table,
		Batch:   batch,
		cols:    columns,
		colIdxs: colIdxs,
		buf:     make([]any, 0, len(columns)*batch),
	}
}

func (s *BulkSink) Submit(ctx context.Context, rows []Row) error {
	if len(rows) == 0 {
		return nil
	}
	args := make([]any, 0, len(s.cols)*len(rows))
	var sb bulkBuilder
	sb.WriteString("INSERT INTO `")
	sb.WriteString(s.Table)
	sb.WriteString("` (")
	sb.WriteQuoted(s.cols)
	sb.WriteString(") VALUES ")
	rowPH := sb.RowPlaceholder(len(s.cols))
	for i, row := range rows {
		if i > 0 {
			sb.WriteString(", ")
		}
		sb.WriteString(rowPH)
		for _, idx := range s.colIdxs {
			var v any
			if idx >= 0 && idx < len(row) {
				v = row[idx]
			}
			args = append(args, normalizeArg(v))
		}
	}
	if _, err := s.DB.ExecContext(ctx, sb.String(), args...); err != nil {
		return fmt.Errorf("bulk insert %s: %w", s.Table, err)
	}
	return nil
}

func (s *BulkSink) Close() error { return nil }

func normalizeArg(v any) any {
	switch x := v.(type) {
	case nil:
		return nil
	default:
		return x
	}
}

type bulkBuilder struct {
	buf []byte
}

func (b *bulkBuilder) WriteString(s string) { b.buf = append(b.buf, s...) }
func (b *bulkBuilder) String() string       { return string(b.buf) }
func (b *bulkBuilder) WriteQuoted(cols []string) {
	for i, c := range cols {
		if i > 0 {
			b.buf = append(b.buf, ", `"...)
		} else {
			b.buf = append(b.buf, '`')
		}
		b.buf = append(b.buf, c...)
		b.buf = append(b.buf, '`')
	}
}
func (b *bulkBuilder) RowPlaceholder(n int) string {
	out := make([]byte, 0, n*3)
	out = append(out, '(')
	for i := 0; i < n; i++ {
		if i > 0 {
			out = append(out, ", "...)
		}
		out = append(out, '?')
	}
	out = append(out, ')')
	return string(out)
}


type RedStubBulkSink struct {
	*BulkSink
}

func NewRedBagStubBulkSink(db *sql.DB, table string, columns []string, colIdxs []int, batch int) *RedStubBulkSink {
	return &RedStubBulkSink{
		BulkSink: NewBulkSink(db, table, columns, colIdxs, batch),
	}
}

func (s *RedStubBulkSink) Submit(ctx context.Context, rows []Row) error {
	if len(rows) == 0 {
		return nil
	}
	args := make([]any, 0, len(s.cols)*len(rows))
	var sb bulkBuilder
	sb.WriteString("INSERT INTO `")
	sb.WriteString(s.Table)
	sb.WriteString("` (")
	sb.WriteQuoted(s.cols)
	sb.WriteString(") VALUES ")
	rowPH := sb.RowPlaceholder(len(s.cols))
	for i, row := range rows {
		if i > 0 {
			sb.WriteString(", ")
		}
		sb.WriteString(rowPH)
		for _, idx := range s.colIdxs {
			var v any
			if idx >= 0 && idx < len(row) {
				v = row[idx]
			}
			args = append(args, normalizeArg(v))
		}
	}
	sb.WriteString(" ON DUPLICATE KEY UPDATE ")
	for i, col := range s.cols {
		if i > 0 {
			sb.WriteString(", ")
		}

		sb.WriteString("`")
		sb.WriteString(col)
		sb.WriteString("`")
	
		sb.WriteString("=VALUES(`")
		sb.WriteString(col)
		sb.WriteString("`)")
	}
	if _, err := s.DB.ExecContext(ctx, sb.String(), args...); err != nil {
		return fmt.Errorf("bulk insert %s: %w", s.Table, err)
	}
	return nil
}
