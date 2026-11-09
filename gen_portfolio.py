# -*- coding: utf-8 -*-
"""作品集看板生成器：读真实数据形状 → 生成仿真数据 → 输出单文件 index.html。

真实数字不落盘到成品——CSV 只在本机作底稿，输出全部为缩放+扰动的仿真值。
"""
import csv, json, random, io, os

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(20261109)


def read_csv(path):
    with io.open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def jitter(v, pct):
    return v * (1 + rng.uniform(-pct, pct))


def cost_series():
    """58 天成本/消耗/单位成本，全部转仿真。"""
    rows = read_csv(os.path.join(HERE, "sim_cost.csv"))
    out = []
    base_unit = None
    for r in rows:
        unit = float(r["unit_cost"])
        if base_unit is None:
            base_unit = unit
        out.append({
            "d": r["dt"],
            # 总成本：×0.42 缩放 + 4% 抖动，取整到 5
            "cost": int(round(jitter(float(r["cost_usd"]) * 0.42, 0.04) / 5) * 5),
            "p_cost": int(round(jitter(float(r["p_cost"]) * 0.42, 0.04) / 5) * 5),
            "s_cost": int(round(jitter(float(r["s_cost"]) * 0.42, 0.05) / 5) * 5),
            # 积分消耗：折成「万积分」保留 1 位；与成本同用 0.42 缩放，保持消耗/成本比的真实形状
            "p_cr": round(jitter(int(r["purchase_net"]) / 10000.0 * 0.42, 0.03), 1),
            "s_cr": round(jitter(int(r["subscription_net"]) / 10000.0 * 0.42, 0.05), 1),
            "g_cr": round(jitter(int(r["gift_net"]) / 10000.0 * 0.42, 0.03), 1),
            # 单位积分成本：指数化（首日=100）+ 2% 抖动
            "unit_idx": round(jitter(unit / base_unit * 100, 0.02), 1),
        })
    return out


def mem_series():
    """订阅上线 17 天会员/收入/MRR。"""
    rows = read_csv(os.path.join(HERE, "sim_membership.csv"))
    out = []
    for r in rows:
        out.append({
            "d": r["date"],
            "members": max(1, int(round(jitter(int(r["new_members"]) * 0.6, 0.05)))),
            "net_rev": int(round(jitter(float(r["net_rev"]) * 0.37, 0.04) / 10) * 10),
            "mrr": int(round(jitter(float(r["mrr"]) * 0.37, 0.04) / 10) * 10),
        })
    return out


def to_index(vals, base=None):
    b = vals[base] if base is not None else vals[0]
    return [round(v / b * 100, 1) if b else None for v in vals]


cost = cost_series()
mem = mem_series()

# 订阅 ROI 指数（以订阅上线首日为 100）
sub_rev_idx = to_index([m["net_rev"] for m in mem])
sub_cost_idx = to_index([c["s_cost"] for c in cost[-len(mem):]])
# 购买 ROI 指数（全窗口，首日=100）
p_equiv = [c["p_cr"] * 100 for c in cost]  # 万积分 → 等效金额（1万积分=$100 面值口径）
p_equiv_idx = to_index(p_equiv)
p_cost_idx = to_index([c["p_cost"] for c in cost])

# KPI 汇总
tot_rev = sum(m["net_rev"] for m in mem)
tot_members = sum(m["members"] for m in mem)
tot_credits = sum(c["p_cr"] + c["s_cr"] + c["g_cr"] for c in cost)
sub_cost_total = sum(c["s_cost"] for c in cost)
p_ratio = round(sum(p_equiv) / max(1, sum(c["p_cost"] for c in cost)), 2)
sub_ratio = round(tot_rev / max(1, sub_cost_total), 1)

data = {
    "cost": cost,
    "mem": mem,
    "series": {
        "sub_rev_idx": sub_rev_idx,
        "sub_cost_idx": sub_cost_idx,
        "p_equiv_idx": p_equiv_idx,
        "p_cost_idx": p_cost_idx,
    },
    "kpi": {
        "tot_rev": tot_rev, "tot_members": tot_members,
        "tot_credits": round(tot_credits, 1),
        "sub_ratio": sub_ratio, "p_ratio": p_ratio,
        "mrr_last": mem[-1]["mrr"],
        "days_cost": len(cost), "days_mem": len(mem),
    },
    "launch": "2026-10-21",
}

with io.open(os.path.join(HERE, "portfolio_data.json"), "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("cost days:", len(cost), "| mem days:", len(mem))
print("KPI 仿真值: 累计净收入 $%s | 新增会员 %s | 累计核算 %s 万积分 | 订阅收入成本比 %s | 购买收入成本比 %s"
      % (tot_rev, tot_members, round(tot_credits, 1), sub_ratio, p_ratio))
