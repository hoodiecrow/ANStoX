
# ANStoX

A set of Python scripts to convert annotated source to code, tests, and documentation in Markdown, (La)TeX, and html flavors.

(I started out with AWK scripts, but AWK inexplicably freezed while processing this document, so I rewrote them.)

This method uses one or more `` .ans `` (ANnotated Source) files which are filtered through one of the Python filters and mashed together to form a document. The idea is that each `` .ans `` file contains a number of code snippets, each with a short or long bit of documentation, and a number of test cases for it.

Examples:

```
python3 anstocode.py alpha.ans beta.ans >thefile.c

python3 anstotest.py alpha.ans beta.ans >thefile.test

python3 anstomd.py alpha.ans beta.ans >README.md

python3 anstohtml.py alpha.ans beta.ans >thepage.html

python3 anstotex.py alpha.ans beta.ans >middle.tex

cat preamble.tex middle.tex end.tex >thedoc.tex
```

In these cases, `` alpha.ans `` and `` beta.ans `` are source files containing documentation, test tags, and code tags.

The code tags are printed to the code file by `` anstocode.py `` and the test tags to the test file by `` anstotest.py ``.

The documentation and content of the code tags are printed in different ways to the README document by `` anstomd.py ``, to the thedoc document by `` anstotex.py ``, and to the thepage document by `` anstohtml.py ``. These three scripts also use a file called `` dict.txt `` which is a special case which will be explained below.


---


Note that unlike the html and Markdown documents, the middle.tex document is incomplete. It needs at least a preamble and a begin and end for the document, which you will have to supply (I have no way of knowing what you need regarding that).


---


The code in these scripts grew out of Graham Marlow's [Markdown Rendering with Awk](https://www.mgmarlow.com/words/2024-03-23-markdown-awk/). The Literate Programming concept by Donald E Knuth was of course a major inspiration.

## Tags

### Documentation text

The original conception had an `` MD `` tag for documentation text. I was already writing this document when I realized that it was better to have the documentation text as free text, without any tags. I'm still getting used to it, but it's definitely a change for the better.

```

This is a short docu text.

```

The documentation text is processed for styling and output by the `` anstomd.py ``, `` anstotex.py ``, and `` anstohtml.py `` scripts.

Remember to put empty lines before and after paragraphs, otherwise the paragraphs will bleed into each other.

### Prototype table

The `` PR `` tag is supposed to contain a single line with table header, semicolon, parameter names and type codes delimited by spaces, and the symbol -> and a type code for the return value. The type codes are resolved by the dictionary loaded from dict.txt (see last section). As a result, a table is inserted into the documentation document. It is very useful to me, but I'm not sure if anyone else would find it useful. In case someone asks, I'll document it further.

```
PR(
my function;a foo -> foo
PR)
```

<table border=1><thead><tr><th colspan=2 align="left">my function</th></tr></thead><tr><td>a</td><td>bar</td></tr><tr><td><i>Returns:</i></td><td>bar</td></tr></table>

### Code

The `` CB `` tag is for code, regardless of coding language.

```
CB(
#include <stdio.h>

int main (void) {
    printf("Hello, world");
    return 0;
}
CB)
```

```
#include <stdio.h>

int main (void) {
    printf("Hello, world");
    return 0;
}
```

The contents of the `` CB `` tag are output without further processing by all the scripts except `` anstotest.py ``, which does not output it, and `` anstohtml.py ``, which does basic htmlification of `` & ``, `` < ``, `` > ``, `` " ``, and `` ' ``. `` anstomd.py ``, `` anstotex.py ``, and `` anstohtml.py `` add elements around the tag's output, suitable for presenting code (i.e. triple backticks for Markdown, the `` lstlisting `` environment for (La)TeX, pre and code for html).

### Verbatim

The `` VB `` tag is for text that should be output with no extra processing (except basic htmlification by `` anstohtml.py ``) and presented with triple backticks for Markdown, the `` verbatim `` environment for (La)TeX, and pre for html. The contents of the tag aren't output by `` anstocode.py `` or `` anstotest.py ``.

### Test cases

The `` TT `` tag is used for test case code which will be output by `` anstotest.py `` alone. The `` anstotest.py `` script is geared towards the `` tcltest `` engine, but should be possible to convert to other test engines by editing the initial and final output blocks in the script.

```
TT(
::tcltest::test foobar-1.0 {try the foobar} -body {
   ...
} -output "..."
TT)
```


---


### Pulled text

The `` PT `` tag is different. It isn't treated as a content tag. Instead, one puts it around a short range of documentation text. The point of using it is that it adds formatting around the text within it: for Markdown it is a preceding and a succeeding horizontal rule; for (La)TeX it's the beginning and end of the `` pulledtext `` environment, for html it is the element aside. The end result is a bit of text which is marked off, like an aside.


---


### Lists

The `` IT `` and `` EN `` tags _at the beginning of the line_ renders the line as a bulleted or a numbered list item, respectively.

Example:

```
IT fee
IT fie
IT foe
```

* fee
* fie
* foe

The `` DL `` tag renders the line as a definition list item. The token LD separates the term from the definition.

```
DL an item LD with a definition.
DL another item LD with mostly the same definition.
```

1. an item  
with a definition.
1. another item  
with mostly the same definition.

The definition list is faked in Markdown, and is not guaranteed to work everywhere.

## Headings

The headings tags are the same as in html, `` H1 `` to `` H6 ``, only you put them at the start of the line, with the heading text following. They are translated to hash groups for Markdown, to different heading elements for (La)TeX, and to the obvious elements in html.

```
H4 A title
```

#### A title

### IG, EM and KB

These three beginning of the line tags:

1. import a graphics element (an image)
1. wrap the entire line in italics elements
1. wrap the entire line in keyboard font elements

```
IG /images/myimage.png

EM This line will be in italics
```

![#](images/myimage.png)

_This line will be in italics_

### IF, IX, NI

`` IF `` imports an image, but puts it in a float and adds a caption.

```
IF /images/myimage.png Look how pretty
```

![#](images/myimage.png "Look how pretty")

(It seems that it needs to be styled with CSS to be visible in html.)

`` IX `` and `` NI `` are mostly useful for translation to (La)TeX.

`` IX `` makes an index entry from the text that follows it. `` NI `` puts a `` \noindent `` in front of the line.

## Styling

### Appearance

`` B ``{ ... } renders text bold. `` E ``{ ... } renders text in italics. `` K ``{ ... } renders text in keyboard font.

```
first I B{was ...}, then I E{was ...}, but then I K{was ...}
```

first I __was ...__, then I _was ..._, but then I `` was ... ``

### Links, footnotes, and references

`` F ``{ ... } creates a (La)TeX footnote, or just a parenthesized bit of text in Markdown or html. `` R ``{ ... }{ ... } inserts a page reference text in (La)TeX and a link in Markdown or html.

```
dolor R{sit amet}{toc-label}, consectetur
```

is rendered

```
dolor sit amet (see page \pageref{toc-label}), consectetur
```

in (La)TeX,

```
dolor [sit amet](https://github.com/hoodiecrow/ConsTcl#toc-label), consectetur
```

in Markdown (clearly some personalizing is necessary: edit the baseURL variable), and

```
dolor <a href="https://github.com/hoodiecrow/ConsTcl#toc-label">sit amet</a>, consectetur
```

in html (ditto).

`` S ``{ ... }{ ... } is the same as `` R ``, but adds elements for keyboard font around the anchor.

`` L ``{ ... }{ ... } is like `` R ``, but for an external link.

```
dolor L{sit amet}{http://site/dir/index.html}, consectetur
```

is rendered

```
dolor sit amet\footnote{See \texttt{http://site/dir/index.html}}, consectetur
```

in (La)TeX,

```
dolor [sit amet](http://site/dir/index.html), consectetur
```

in Markdown, and

```
dolor <a href="http://site/dir/index.html">sit amet</a>, consectetur
```

in html.

`` W ``{ ... }{ ... } is like `` L ``, but for a link to Wikipedia. The contents of the second capture field is supposed to be the part of the URL after `` https://en.wikipedia.org/wiki/ ``. Example:

```
W{Ann Arbor, Michigan}{Ann_Arbor,_Michigan}
```

[Ann Arbor, Michigan](https://en.wikipedia.org/wiki/Ann_Arbor,_Michigan)

## dict.txt

Is a file containing a dictionary that I use to construct prototype tables for procedures in my code. You will probably not need or want it, so just add a `` dict.txt `` containing the text "`` foo -> bar ``" or something like that (or just take the `` dict.txt `` from the repository). With some editing of the scripts, the use for it can be removed. I still need it, so I'm not going to remove it myself.


