from datetime import datetime, timedelta
from sqlalchemy import func
from . import db
import logging


class ApiStatus(db.Model):
    __tablename__ = "api_status"

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(100), nullable=False)
    api_url = db.Column(db.String(500), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    status_text = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500))
    response_time = db.Column(db.Float)  # Response time in seconds
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "api_name": self.api_name,
            "api_url": self.api_url,
            "api_last_status_code": self.status_code,
            "api_status_text": self.status_text,
            "api_last_msg": self.message,
            "response_time": self.response_time,
            "checked_at": self.checked_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        }


class ApiStatusHistory(db.Model):
    __tablename__ = "api_status_history"

    id = db.Column(db.Integer, primary_key=True)
    api_name = db.Column(db.String(100), nullable=False)
    api_url = db.Column(db.String(500), nullable=False)
    status_code = db.Column(db.Integer, nullable=False)
    status_text = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(500))
    response_time = db.Column(db.Float)  # Response time in seconds
    checked_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "api_name": self.api_name,
            "api_url": self.api_url,
            "status_code": self.status_code,
            "status_text": self.status_text,
            "message": self.message,
            "response_time": self.response_time,
            "checked_at": self.checked_at.strftime("%Y-%m-%d %H:%M:%S UTC"),
        }

    @classmethod
    def get_uptime_percentage(cls, api_name, days=30):
        """Calculate uptime percentage for the last X days"""
        start_date = datetime.utcnow() - timedelta(days=days)
        total_checks = cls.query.filter(
            cls.api_name == api_name, cls.checked_at >= start_date
        ).count()

        successful_checks = cls.query.filter(
            cls.api_name == api_name,
            cls.checked_at >= start_date,
            cls.status_code == 200,
        ).count()

        return (successful_checks / total_checks * 100) if total_checks > 0 else 0

    @classmethod
    def get_response_time_stats(cls, api_name, days=1):
        """Get response time statistics for the last X days"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            stats = (
                db.session.query(
                    func.avg(cls.response_time).label("avg"),
                    func.min(cls.response_time).label("min"),
                    func.max(cls.response_time).label("max"),
                )
                .filter(
                    cls.api_name == api_name,
                    cls.checked_at >= start_date,
                    cls.response_time.isnot(None),  # Exclude NULL response_time values
                )
                .first()
            )

            # If no stats found or all values are None, return zeros
            if not stats:
                return {"avg": 0.0, "min": 0.0, "max": 0.0}

            # Safely convert and round values, defaulting to 0.0 if None
            return {
                "avg": round(float(stats.avg or 0.0), 3),
                "min": round(float(stats.min or 0.0), 3),
                "max": round(float(stats.max or 0.0), 3),
            }
        except Exception as e:
            logging.error(f"Error calculating response time stats: {str(e)}")
            return {"avg": 0.0, "min": 0.0, "max": 0.0}

    @classmethod
    def get_history_data(cls, api_name, hours=24):
        """Get historical data for graphs"""
        start_date = datetime.utcnow() - timedelta(hours=hours)
        history = (
            cls.query.filter(cls.api_name == api_name, cls.checked_at >= start_date)
            .order_by(cls.checked_at.asc())
            .all()
        )

        return [
            {
                "timestamp": entry.checked_at.strftime("%Y-%m-%d %H:%M:%S"),
                "status_code": entry.status_code,
                "response_time": entry.response_time,
            }
            for entry in history
        ]


class UserPreferences(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(db.Integer, primary_key=True)
    notification_email = db.Column(db.String(200))
    notification_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class GlobalSettings(db.Model):
    __tablename__ = "global_settings"

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(500))
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    @classmethod
    def get_setting(cls, key, default=None):
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default

    @classmethod
    def set_setting(cls, key, value):
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
