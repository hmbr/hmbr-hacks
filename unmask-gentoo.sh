#!/bin/bash
#
#@author: HŽlder M‡ximo Botter Ribas <helderribas gmail.com>
#


source /sbin/functions.sh

iniciou="nao"
KEYWORDS="/etc/portage/package.keywords"


if [[ "`whoami`" != "root" ]]; then
        eerror "Root Privilegies Required"
        exit 1
fi


if [[ -z "$1" ]]; then
        ewarn "Use: ./$0 <package>"
        exit 2
fi

p_mask(){
	ebegin "Unmasking $pacote"
	echo "=$pacote" >>/etc/portage/package.unmask
	eend
}

p_key(){	
	ebegin "Putting Keyword ~* for $pacote"
	echo "=$pacote ~*" >>$KEYWORDS
	eend

}

p_miss_key(){
	ebegin "Putting Keyword -* for $pacote"
	echo "${pacote/-[0-9]*} -*" >>$KEYWORDS
	eend

}

#testing if KEYWORDS="/etc/portage/package.keywords" is a directory (thanks deusr@freenode for the ideia)

if [[ -d $KEYWORDS ]]; then
        KEYWORDS="$KEYWORDS/unmask"
fi

einfo "Looking for masked packages at `date +%d_%m_%Y` for $@"
for i in $@; do
	while true ;
	do
		verificacao=`emerge -p $i  | grep masked\ by:\ ~ | tail -n 1`
		pacote=`echo $verificacao| cut -d" " -f2`
		if [[ -n $pacote ]]; then
			if [[ $verificacao == *package.mask* ]]; then
				p_mask
			fi
			if [[ $verificacao == *keyword* ]]; then
				if [[ $verificacao == *missing* ]]; then
					p_miss_key
				else
					p_key
				fi
			fi
			else
				break
			iniciou="yes"
		fi
	done
done

exit 0