function jaccardSimilarity(a = [], b = []) {
  const setA = new Set(a);
  const setB = new Set(b);
  const intersection = [...setA].filter((v) => setB.has(v)).length;
  const union = new Set([...setA, ...setB]).size || 1;
  return intersection / union;
}

function departmentScore(depA, depB) {
  return depA === depB ? 0.15 : 0.05;
}

function compatibilityScore({ interestsA, interestsB, departmentA, departmentB }) {
  const interestComponent = jaccardSimilarity(interestsA, interestsB) * 85;
  const deptComponent = departmentScore(departmentA, departmentB) * 100;
  return Math.min(100, Math.round(interestComponent + deptComponent));
}

module.exports = { compatibilityScore };
