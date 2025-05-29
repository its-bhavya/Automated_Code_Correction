def lcs_length(s, t):
    dp = {}

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                if i == 0 or j == 0:
                    dp[i, j] = 1
                else:
                    dp[i, j] = dp.get((i - 1, j - 1), 0) + 1
            else:
                dp[i, j] = 0

    return max(dp.values()) if dp else 0