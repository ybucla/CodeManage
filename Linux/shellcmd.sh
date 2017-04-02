## awk 匹配模式 group
echo '# Num of 131' |awk 'match($0, /([0-9]+)/, ary) {print ary[1]}'
echo '# Num of 131' | awk 'BEGIN {sum=0}; match($0, /([0-9]+)/, a) {sum += a[1]}; END{print sum}'

## for 循环
for((i = 1;i<=20;i++));do ./bin/run $i; done
for i in `ls`; do echo $i; done
for i in {2..10};do echo $i;done
for i in {2..10};do printf $i'\t';done

## split 输出后缀为数字，前缀为pre_，按行输出
split -d -l 3 input pre_

## vi 设置书签
# ma			set mark a at current cursor location
# 'a			jump to line of mark a (first non-blank character in line)
# `a			jump to position (line and column) of mark a
# d'a			delete from current line to line of mark a
# d`a			delete from current cursor position to position of mark a
# c'a			change text from current line to line of mark a
# y`a			yank text to unnamed buffer from cursor to position of mark a
:marks			list all the current marks
:marks aB		list marks a, B
:Ctrl + O: 上一个编辑位置

## vi 切换多个打开的文件 switch two files:
:n			Next file
:p			Previous file

## vi 执行命令
:!cmd

## less
:&pattern - 仅显示匹配模式的行，而不是整个文件
