use chrono::{DateTime, Utc, Duration};

/// Calculate the date one gigasecond (10^9 seconds) from a given date.
pub fn after(start: DateTime<Utc>) -> DateTime<Utc> {
    start + Duration::seconds(1_000_000_000)
}
