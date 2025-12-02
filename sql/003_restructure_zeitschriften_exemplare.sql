-- Migration: Umbau Zeitschrift/Exemplar-Struktur
-- Vorher: zeitschriften nur mit Titel, alle Ausgabedetails/Barcodes in exemplare
-- Nachher: zeitschriften speichert die konkrete Ausgabe (Titel, Erscheinungsdatum, Ausgabe),
--          exemplare zählt nur noch verfügbare/gesamte Exemplare dieser Ausgabe

SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS;
SET FOREIGN_KEY_CHECKS = 0;

-- Backup erstellen (falls Daten vorhanden)
CREATE TABLE IF NOT EXISTS zeitschriften_backup_20251202 AS SELECT * FROM zeitschriften;
CREATE TABLE IF NOT EXISTS exemplare_backup_20251202 AS SELECT * FROM exemplare;
CREATE TABLE IF NOT EXISTS ausleihen_backup_20251202 AS SELECT * FROM ausleihen;

-- Zeitschriften-Tabelle um Ausgabe-Details erweitern
ALTER TABLE zeitschriften
  ADD COLUMN IF NOT EXISTS barcode varchar(255) UNIQUE,
  ADD COLUMN IF NOT EXISTS ausgabe_heftnummer varchar(255) DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS erscheinungsdatum date DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS aktiv tinyint(1) DEFAULT 1;

-- Neue exemplare-Tabelle als Bestandszähler (eine Zeile pro Zeitschrift)
DROP TABLE IF EXISTS exemplare_new;
CREATE TABLE exemplare_new (
  ExemplarID int(11) NOT NULL AUTO_INCREMENT,
  ZeitschriftID int(11) NOT NULL,
  Bestand int(11) NOT NULL DEFAULT 0,
  Verfuegbar int(11) NOT NULL DEFAULT 0,
  Aktiv tinyint(1) DEFAULT 1,
  PRIMARY KEY (ExemplarID),
  UNIQUE KEY uniq_zeitschrift (ZeitschriftID),
  CONSTRAINT exemplare_new_ibfk_1 FOREIGN KEY (ZeitschriftID) REFERENCES zeitschriften (ZeitschriftID) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Migration bestehender Daten: auf Bestand/Verfügbarkeit je Zeitschrift aggregieren
INSERT INTO exemplare_new (ZeitschriftID, Bestand, Verfuegbar, Aktiv)
SELECT 
  e.ZeitschriftID,
  COUNT(*) AS Bestand,
  GREATEST(
    COUNT(*) - COALESCE(SUM(CASE WHEN a.Rueckgabedatum IS NULL THEN 1 ELSE 0 END), 0),
    0
  ) AS Verfuegbar,
  CASE WHEN MAX(e.Aktiv) = 0 THEN 0 ELSE 1 END AS Aktiv
FROM exemplare e
LEFT JOIN ausleihen a ON e.ExemplarID = a.ExemplarID
GROUP BY e.ZeitschriftID;

-- Ausleihen auf die neuen Exemplar-IDs mappen
CREATE TEMPORARY TABLE exemplar_map AS
SELECT 
  e.ExemplarID AS old_id,
  agg.ExemplarID AS new_id
FROM exemplare e
JOIN exemplare_new agg ON agg.ZeitschriftID = e.ZeitschriftID;

UPDATE ausleihen a
JOIN exemplar_map m ON a.ExemplarID = m.old_id
SET a.ExemplarID = m.new_id;

DROP TEMPORARY TABLE IF EXISTS exemplar_map;

-- Alte exemplare-Tabelle durch neue ersetzen
DROP TABLE IF EXISTS exemplare;
RENAME TABLE exemplare_new TO exemplare;

-- Abschluss
SELECT 'Migration erfolgreich. Exemplare: ', COUNT(*) FROM exemplare;
SELECT 'Zeitschriften im Katalog: ', COUNT(*) FROM zeitschriften;

SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
