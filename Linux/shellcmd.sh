# awk 匹配模式 group
echo '# Num of 131' |awk 'match($0, /([0-9]+)/, ary) {print ary[1]}'
echo '# Num of 131' | awk 'BEGIN {sum=0}; match($0, /([0-9]+)/, a) {sum += a[1]}; END{print sum}'

