echo -e -n "##
## EPITECH PROJECT, 2019
## C Pool $1
## File description:
## Makefile
##

NAME = $2

FILES = " > "CPool_$1_2019/Makefile"
tree -i -f "CPool_$1_2019" | cat | grep "\.c" | sed -z "s/\n/ @£/g" | sed "s/ @£$//g" | tr "@" "\\" | sed -z "s/£/\n    /g" | sed "s/CPool_$1_2019\///g" >> "CPool_$1_2019/Makefile"
echo -e "

all :	\$(NAME)

\$(NAME):
	gcc -o \$(NAME) \$(FILES)

clean:
	rm -f *.o

fclean:	clean
	rm -f \$(NAME)

re:	fclean all

prepush:	fclean
	rm -f *# *~ ./*/*# ./*/*~ ./*/*/*# ./*/*/*~

tree:	prepush
	tree -a -I .git

push:	prepush
	rm -f *#
	rm -f *~
	rm -f .#*
	git add --all
	git commit -m \"auto-push\"
	git push origin master

pull:
	git pull origin master

sync:	pull	push" >> "CPool_$1_2019/Makefile"
emacs "CPool_$1_2019/Makefile"
