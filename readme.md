Majsoul Record
========================

Simple majsoul record parser

### Usage

```
http://hostname/uuid/<uuid>
http://hostname/uuid-csv/<uuid>
http://hostname/uuid-raw/<uuid>
```

### Development

1. Set env vars
```ini
MAJSOUL_PASSWORD=your-password
MAJSOUL_USERNAME=your-email
MAJSOUL_HOST=https://game.maj-soul.com
FLASK_APP=main
FLASK_DEBUG=1
```

2. Run server
```bash
pipenv run server
```

### License

MIT
