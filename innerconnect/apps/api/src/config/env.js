const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  port: process.env.PORT || 4000,
  jwtSecret: process.env.JWT_ACCESS_SECRET || 'change-me',
  companyDomain: process.env.COMPANY_EMAIL_DOMAIN || 'company.com',
  databaseUrl: process.env.DATABASE_URL || ''
};
