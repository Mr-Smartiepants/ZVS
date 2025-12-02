-- Migration: add display_name to benutzer and set NULL default (MySQL syntax)
ALTER TABLE benutzer
  ADD display_name VARCHAR(255) NULL;

-- Optional: create an index for lookups by display_name (no IF NOT EXISTS in MySQL)
CREATE INDEX idx_benutzer_display_name ON benutzer(display_name(100));
