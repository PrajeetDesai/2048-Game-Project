const { compatibilityScore } = require('../utils/matching');

function scoreCandidate(req, res) {
  const { me, candidate } = req.body;
  const score = compatibilityScore({
    interestsA: me.interests,
    interestsB: candidate.interests,
    departmentA: me.department,
    departmentB: candidate.department
  });

  return res.json({ score, matched: score >= 55 });
}

module.exports = { scoreCandidate };
