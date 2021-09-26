Majsoul Record
========================

Simple majsoul record parser

### Usage

```
https://majsoul-record.herokuapp.com/uuid/<uuid>
https://majsoul-record.herokuapp.com/uuid-csv/<uuid>
https://majsoul-record.herokuapp.com/uuid-raw/<uuid>
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
