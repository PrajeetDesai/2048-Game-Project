const router = require('express').Router();
const { requireAuth } = require('../middleware/auth');
const { scoreCandidate } = require('../controllers/matchController');

router.post('/score', requireAuth, scoreCandidate);

module.exports = router;
