#!/bin/bash
export PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin;

#### TRAP
# trap ctrl-c and call ctrl_c()
# trap ctrl_c INT

# function ctrl_c() {
        # echo "** Trapped CTRL-C"
# }

# for i in `seq 1 5`; do
    # sleep 1
    # echo -n "."
# done


# trap ctrl-c and call ctrl_c()
# trap ctrl_c INT

# function ctrl_c() {
    # echo 
    # echo "Ctrl-C by user"
    # do the jobs
    # exit
# }
#####

## Dir check & old log files cleanup
WD=/var/tmp/os_patch_val;
##
## Functions to take precheck & postcheck outputs
function precheck {
###
echo "----------------------------------------------------"
if [ -d $WD ]
then
rm $WD/*.out;
else
mkdir -p $WD;
echo -e "'$WD'- created for collecting data\n";
fi
echo -e "Saving $WD/pre_Name-IP.out .......";
#
ip addr show |awk '/inet /{print $NF,$2;}' |while read iface IP ;do AIP=$IP;IP=${IP%/*};HOST=$(nslookup $IP|awk '/name =/{print $NF;}');printf "%-20s %-20s %-20s\n" "$iface" "$AIP" "$HOST" >> $WD/pre_Name-IP.out;done;
###
echo -e "Saving $WD/pre_FS-Mount.out ......";
#
df -hPT | egrep -vi '/\nas/\common|/\nas/\usr|/\nas/\orasoft|/\nas/\util|/\nas/\CDs|/\nas/\images|Mounted on' | awk '{print $1,"\t",$2,"\t",$3,"\t",$7}'  | sort > $WD/pre_FS-Mount.out;
###
echo -e "Saving $WD/pre_IP-Link.out .......";
#
ip -o link show | grep -v loop | grep UP | cut -d':' -f 2-20 | sort -n > $WD/pre_IP-Link.out;
###
echo -e "Saving $WD/pre_IP-Addr.out .......";
#
ip -o addr show | cut -d':' -f 2-20 | cut -d'\' -f1| sort -n > $WD/pre_IP-Addr.out;
###
echo -e "Saving $WD/pre_IP-Route.out ......";
#
ip route show | sort -n > $WD/pre_IP-Route.out;
#
echo -e "\nCollection completed under '$WD'.."
echo "----------------------------------------------------"
}

function postcheck {
echo "----------------------------------------------------"
if [ -d $WD ] && [[ `ls $WD/pre*.out 2>/dev/null|wc -l` -eq 5 ]]
then
echo -e "'$WD' and preout files exists.....\n"
###
echo -e "Saving $WD/post_Name-IP.out ......";
#
ip addr show |awk '/inet /{print $NF,$2;}' |while read iface IP ;do AIP=$IP;IP=${IP%/*};HOST=$(nslookup $IP|awk '/name =/{print $NF;}');printf "%-20s %-20s %-20s\n" "$iface" "$AIP" "$HOST" >> $WD/post_Name-IP.out;done;
###
echo -e "Saving $WD/post_FS-Mount.out .....";
#
df -hPT | egrep -vi '/\nas/\common|/\nas/\usr|/\nas/\orasoft|/\nas/\util|/\nas/\CDs|/\nas/\images|Mounted on' | awk '{print $1,"\t",$2,"\t",$3,"\t",$7}'  | sort > $WD/post_FS-Mount.out;
###
echo -e "Saving $WD/post_IP-Link.out ......";
#
ip -o link show | grep -v loop | grep UP | cut -d':' -f 2-20 | sort -n > $WD/post_IP-Link.out;
###
echo -e "Saving $WD/post_IP-Addr.out ......";
#
ip -o addr show | cut -d':' -f 2-20 | cut -d'\' -f1| sort -n > $WD/post_IP-Addr.out;
###
echo -e "Saving $WD/post_IP-Route.out .....";
#
ip route show | sort -n > $WD/post_IP-Route.out;
###
echo -e "\nCollection completed under '$WD'.."
echo "----------------------------------------------------"
else
echo -e "Cannot execute Post Collection.
Check the $WD for Preout files.... "
echo "----------------------------------------------------"
fi
}

precheck; sleep 10;
postcheck;