// ===== 任务奖励计算 =====
function calculateMissionReward(state, mission) {
    let reward = mission.baseReward;
    if (state) {
        reward += (state.level || 1) * 10;
    }
    return reward;
}
