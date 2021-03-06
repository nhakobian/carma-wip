# Remove everything between the BEGIN and END Index comments.
/<\!--.*WIP BEGIN Index/,/<\!--.*WIP END Index/d
# Just remove the rest of the BEGIN and END comments.
/<\!--.*WIP.*-->/d
# Too bad there's no way to make sed ignore case!
s?<CODE>??g
s?</CODE>??g
### These two are done later after formatting....
### s?<PRE>??g
### s?</PRE>??g
# Stuff to ignore
s?<HTML[^>]*>??g
s?</HTML[^>]*>??g
s?<HEADER[^>]*>??g
s?</HEADER[^>]*>??g
s?<BODY[^>]*>??g
s?</BODY[^>]*>??g
s?<ISINDEX>??
s?</ADDRESS>??g
s?<NEXTID[^>]*>??g
s?<HR[^>]*>??g
s?<BR[^>]*>??g
# character set translations from HTML special chars
s?&gt.?>?g
s?&lt.?<?g
# Paragraph borders
s?<P>??g
s?</P>??g
# Headings
s?<TITLE>[^<]*</TITLE>??g
s?<H\([0-9]\)>[^<]*</H\1>??g
s?<H[0-9]>??g
s?</H[0-9]>??g
# DL is description
s?<DL>??g
s?</DL>??g
s?<DT>??g
s?<DD>??g
# Italics
s?<it>??g
s?</it>??g
# Get rid of Anchors
:pre
s?<A[^>]*>??g
s?</A>??g
