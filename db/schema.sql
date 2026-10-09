CREATE TABLE drugs (
    id                      SERIAL PRIMARY KEY,
    name                    TEXT NOT NULL UNIQUE,
    unit                    TEXT NOT NULL,
    stock                   INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    default_dispense_amount INTEGER CHECK (default_dispense_amount > 0),
    low_stock_threshold     INTEGER CHECK (low_stock_threshold >= 0),
    recount_needed          BOOLEAN NOT NULL DEFAULT FALSE
);
