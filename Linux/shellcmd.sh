# awk 匹配模式 group
echo '# Num of 131' |awk 'match($0, /([0-9]+)/, ary) {print ary[1]}'
echo '# Num of 131' | awk 'BEGIN {sum=0}; match($0, /([0-9]+)/, a) {sum += a[1]}; END{print sum}'

# for 循环
for((i = 1;i<=20;i++));do ./bin/run $i; done
for i in `ls`; do echo $i; done
for i in {2..10};do echo $i;done
for i in {2..10};do printf $i'\t';done

# split 输出后缀为数字，前缀为pre_，按行输出
split -d -l 3 input pre_
