from dataclasses import dataclass


@dataclass
class SMTPParameters:
    host: str
    port: int
    username: str
    password: str
    to: str
