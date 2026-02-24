const router = require('express').Router();
const { requireAuth, requireRole } = require('../middleware/auth');
const { dashboard } = require('../controllers/adminController');

router.get('/dashboard', requireAuth, requireRole(['admin', 'moderator']), dashboard);

module.exports = router;
