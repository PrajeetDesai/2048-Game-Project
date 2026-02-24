const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const { companyDomain, jwtSecret } = require('../config/env');

async function signup(req, res) {
  const { email, password } = req.body;
  if (!email.endsWith(`@${companyDomain}`)) {
    return res.status(400).json({ message: 'Only company email allowed' });
  }

  const passwordHash = await bcrypt.hash(password, 12);
  return res.status(201).json({
    message: 'Signup accepted. Verify OTP sent to email.',
    user: { email, passwordHashPreview: `${passwordHash.slice(0, 12)}...` }
  });
}

function login(req, res) {
  const { userId = 'demo-user-id', role = 'employee' } = req.body;
  const token = jwt.sign({ sub: userId, role }, jwtSecret, { expiresIn: '15m' });
  return res.json({ accessToken: token });
}

module.exports = { signup, login };
