#!/bin/bash                                                                                                                                                                                                                

checkName () {
    dir=$1
    outputs=()
    for file in $(ls -a "${dir}")
    do
        numFiles=$(find "${dir}" -maxdepth 1 -iname "${file}" | wc -l)
        if [ "$numFiles" -gt 1 ]
        then
            fileToAdd="$dir"$(echo "${file}")
            #echo $fileToAdd                                                                                                                                                                                               
            outputs+=( $fileToAdd )
            #echo $outputs                                                                                                                                                                                                 
        fi
    done
    #echo ${outputs[@]}                                                                                                                                                                                                    
    #matchText=$(printf "%s\n" "${outputs[@]}")                                                                                                                                                                            
    #badNames=$(find . -maxdepth 1 | grep -E "\/(-[^\/]*|\.[^\.\/]+|[^\/]*[^A-Za-z\._\/-]+[^\/]*)$|\/[^\/]{15,}$")                                                                                                         
    while read -r line
    do
        #echo $line                                                                                                                                                                                                        
        #echo "SPACERBIG"                                                                                                                                                                                                  
        if [[ -d "${line}" ]]
        then
            outputs+=( "$line""/" )
        else
            outputs+=( "$line" )
        fi
    done < <(find $dir -maxdepth 1 | grep -E "\/(-[^\/]*|\.[^\.\/]+|[^\/]*[^A-Za-z\._\/-]+[^\/]*)$|\/[^\/]{15,}$")

    #echo "SPACER"                                                                                                                                                                                                         
    #echo "${outputs[@]}"                                                                                                                                                                                                  
    #echo "BEFORE PRINTF"                                                                                                                                                                                                  
    printf "%s\n" "${outputs[@]}" | sort -u
    return
}

#echo "$#"                                                                                                                                                                                                                 

#checkDash =`echo $1 | grep -E "^-"`                                                                                                                                                                                       
#echo $checkDash                                                                                                                                                                                                           

if [ "$#" -gt 1 ]
then
    echo "too many arguments" 1<&2
    exit 1
fi

if [[ "$1" =~ ^-.* ]]
then
    echo "too many arguments" 1<&2
    exit 1
fi

if [[ "$1" =~ ^-.* ]]
then
    echo "there's a dash"
    exit 2
fi

D=$1
if [[ -L "${D}" ]]
then
    echo "link, bad directory" 1<&2
    exit 3
elif [[ -d "${D}" ]]
then
    D=$1
#    echo "D is a directory"                                                                                                                                                                                               
elif [[ "$D" == "" ]]
then
    D="."
#    echo "D is ."                                                                                                                                                                                                         
else
    echo "bad directory" 1<&2
    exit 4
fi

if [[ "$D" =~ .*/$ ]]
then
    idk="idk"
else
    D="${D}/"
fi


#echo $D                                                                                                                                                                                                                   

checkName $D