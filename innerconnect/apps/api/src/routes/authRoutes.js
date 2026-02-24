const router = require('express').Router();
const rateLimit = require('express-rate-limit');
const { signup, login } = require('../controllers/authController');

const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 10,
  message: { message: 'Too many login attempts, try again later.' }
});

router.post('/signup', signup);
router.post('/login', loginLimiter, login);

module.exports = router;
