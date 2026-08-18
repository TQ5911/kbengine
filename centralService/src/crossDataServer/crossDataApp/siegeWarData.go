package crossDataApp

import (
	"centralService/src/appLog"
	"database/sql"
	"sync"
	"time"
)

const siegeWarDataRowId = 1

type SiegeWarData struct {
	mu   sync.RWMutex
	data []byte
	db   *sql.DB
}

func NewSiegeWarData(db *sql.DB) *SiegeWarData {
	swd := &SiegeWarData{
		data: make([]byte, 0),
		db:   db,
	}
	swd.loadFromDB()
	return swd
}

func (swd *SiegeWarData) loadFromDB() {
	var data []byte
	err := swd.db.QueryRow("SELECT data FROM siege_war_data WHERE id = ?", siegeWarDataRowId).Scan(&data)
	if err == sql.ErrNoRows {
		appLog.Info("siege war data not found in db")
		return
	}
	if err != nil {
		appLog.Error("load siege war data error:", err.Error())
		return
	}

	swd.mu.Lock()
	defer swd.mu.Unlock()
	swd.data = data
	appLog.Info("load siege war data success, size:", len(data))
}

func (swd *SiegeWarData) Save(data []byte) error {
	now := time.Now().Unix()
	_, err := swd.db.Exec(
		`INSERT INTO siege_war_data (id, data, update_time) VALUES (?, ?, ?)
		 ON DUPLICATE KEY UPDATE data=VALUES(data), update_time=VALUES(update_time)`,
		siegeWarDataRowId, data, now)
	if err != nil {
		appLog.Error("save siege war data error:", err.Error())
		return err
	}

	swd.mu.Lock()
	defer swd.mu.Unlock()
	copied := make([]byte, len(data))
	copy(copied, data)
	swd.data = copied
	appLog.Info("save siege war data success, size:", len(copied))
	return nil
}

func (swd *SiegeWarData) Load() []byte {
	swd.mu.RLock()
	defer swd.mu.RUnlock()
	copied := make([]byte, len(swd.data))
	copy(copied, swd.data)
	return copied
}
