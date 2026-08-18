package domain

type MergeInfo struct {
	SrcServerID int
	DstServerID int
	JobID       string
}

type AccountInfo struct {
	DBID  int64
	IsDst bool
}