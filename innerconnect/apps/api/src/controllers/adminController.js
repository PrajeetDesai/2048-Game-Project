function dashboard(req, res) {
  return res.json({
    totalUsers: 124,
    activeUsers: 89,
    totalMatches: 210,
    reportsCount: 6
  });
}

module.exports = { dashboard };
