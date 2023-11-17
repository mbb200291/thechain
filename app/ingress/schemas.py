from pydantic import BaseModel


class IpList(BaseModel):
    ips: list[str]
