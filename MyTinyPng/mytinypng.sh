#!/bin/bash

dir=#directory#

apikey=#apikey#

pngindex=0

#获取上传文件返回的数据当中的url
parse_json()
{
	value=`echo $1 | sed 's/.*"url":"\(.*\)"}}/\1/g'`
	echo $value
}

compress_file()
{
	for file in `ls $1`; do
		#如果是普通文件
		if [ -f "$1/$file" ]; then
			if [ ${file##*.} == "png" ] || [ ${file##*.} == "PNG" ] || [ ${file##*.} == "jpg" ]; then
				echo "压缩文件$1/$file"

				s=$(curl https://api.tinify.com/shrink \
     --user api:${apikey} \
     --data-binary "@$1/$file")

				url=$(parse_json $s) 

				#如果url不为空下载
				if [ -n "$url" ]; then
					length=$(curl $url \
     --user api:${apikey} \
     --output "$1/$file")
				else
					echo "$s1/$file压缩失败"
				fi
			fi
		#如果是文件夹
		else
			compress_file "$1/$file"
		fi
	done
}

check_filenumber()
{
	for file in `ls $1`; do
		#如果是普通文件
		if [ -f "$1/$file" ]; then
			if [ ${file##*.} == "png" ] || [ ${file##*.} == "PNG" ] || [ ${file##*.} == "jpg" ]; then
				pngindex=`expr $pngindex + 1`
			fi
		#如果是文件夹
		else
			check_filenumber "$1/$file"
		fi
	done
}

main()
{
	echo "请输入以下选项："
	echo "0:查看当前文件夹下的png图片个数"
	echo "1:执行压缩操作"

	read item
	if [ $item == 0 ]; then
		check_filenumber $dir
		echo "图片数:$pngindex";
	elif [ $item == 1 ]; then
		compress_file $dir;
	fi
}

main