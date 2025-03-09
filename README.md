# ANStoX

A set of AWK scripts to convert annotated source to code, tests, and documentation.


This method uses one or more `` .ans `` (ANnotated Source) files which are filtered through one of the AWK-language filters and mashed together to form a document. The idea is that each `` .ans `` file contains a number of code snippets, each with a short bit of documentation for it, and a number of test cases for it.


Examples:

```
awk -f anstocode.awk alpha.ans beta.ans >thefile.scm

awk -f anstotest.awk alpha.ans beta.ans >thefile.test

awk -f anstomd.awk dict.txt alpha.ans beta.ans >README.md

awk -f anstotex.awk dict.txt alpha.ans beta.ans >thedoc.tex

awk -f anstohtml.awk dict.txt alpha.ans beta.ans >thepage.html
```

In these cases, `` alpha.ans `` and `` beta.ans `` are source files containing documentation, test tags, and code tags. The code tags are printed to the code file by `` anstocode.awk ``, the test tags to the test file by `` anstotest.awk ``, and the documentation and content of the code tags are printed in different ways to the readme document by `` anstomd.awk ``, to the thedoc document by `` anstotex.awk ``, and to the thepage document by `` anstohtml.awk ``. The `` dict.txt `` file is a special case which will be explained below.


Note that the .tex document is incomplete: it needs at least a preamble and a begin for the document, which you will have to supply. It does stick an end document to the end, at least.

## Tags
### Documentation text

The original conception had an `` MD `` tag for documentation text. I was already writing this document when I realized that it was better to have the documentation text as free text, without any tags. I'm still getting used to it, but it's definitely a change for the better.

```

This is a short docu text.

```

The documentation text is processed for styling and output by the `` anstomd.awk ``, `` anstotex.awk ``, and `` anstohtml.awk `` scripts.


Remember to put empty lines before and after paragraphs, otherwise the paragraphs will bleed into each other.

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

The contents of the `` CB `` tag are output without further processing by all the scripts except `` anstotest.awk ``. `` anstomd.awk ``, `` anstotex.awk ``, and `` anstohtml `` add elements around the tag's output, suitable for presenting code (i.e. triple backticks for Markdown, the `` lstlisting `` environment for (La)TeX, pre for html).

### Verbatim

The `` VB `` tag is for text that should be output with no extra processing and presented with triple backticks for Markdown, the `` verbatim `` environment for (La)TeX, and pre for html. The contents of the tag aren't output by `` anstocode.awk `` or `` anstotest.awk ``.

### Test cases

The `` TT `` tag is used for test case code which will be output by `` anstotest.awk `` alone. The `` anstotest.awk `` script is geared towards the `` tcltest `` engine, but should be possible to convert to other test engines by editing the BEGIN and END blocks in the script.

```
TT(
::tcltest::test foobar-1.0 {try the foobar} -body {
   ...
} -output "..."
TT)
```


---

### Pulled text

The `` PT `` tag is different. It isn't treated as a content tag. Instead, one puts it around a short range of documentation text. The point of using it is that it adds formatting around the text within it: for Markdown and html it is a preceding and a succeeding horizontal rule; for (La)TeX it's the beginning and end of the `` pulledtext `` environment. The end result is a bit of text which is marked off, like an aside.



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
1.  an item  
with a definition.
1.  another item  
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

 _This line will be in italics_

### IF, IX, NI

These tags are mostly useful for translation to (La)TeX.


`` IF `` imports an image, but puts it in a float and adds a caption.

```
IF /images/myimage.png Look how pretty
```

`` IX `` makes an index entry from the text that follows it. `` NI `` puts a `` \noindent `` in front of the line.

## Styling
### Appearance

`` B ``{ ... } renders text bold. `` E ``{ ... } renders text in italics. `` K ``{ ... } renders text in keyboard font.

```
first I B{was}, then I E{was}, but then I K{was}
```

first I __was__, then I _was_, but then I `` was ``

### Links, footnotes, and references

`` F ``{ ... } creates a (La)TeX footnote, or just a parenthesized bit of text in Markdown or html. `` R ``{ ... }{ ... } inserts a page reference text in (La)TeX and a link in Markdown or html.

```
Lorem ipsum dolor R{sit amet}{toc-label}, consectetur adipiscing elit,
```

Is rendered

```
Lorem ipsum dolor sit amet (see page \pageref{toc-label}), consectetur adipiscing elit,
```

in (La)TeX,

```
Lorem ipsum dolor [sit amet](https://github.com/hoodiecrow/ConsTcl#toc-label), consectetur adipiscing elit,
```

in Markdown (clearly some personalizing is necessary), and

```
Lorem ipsum dolor <a href="https://github.com/hoodiecrow/ConsTcl#toc-label">sit amet</a>, consectetur adipiscing elit,
```

in html (ditto).


`` S ``{ ... }{ ... } is the same as `` R ``, but adds elements for keyboard font around the anchor.


`` L ``{ ... }{ ... } is like `` R ``, but for an external link.

```
Lorem ipsum dolor L{sit amet}{http://site/dir/index.html}, consectetur adipiscing elit,
```

Is rendered

```
Lorem ipsum dolor sit amet\footnote{See \texttt{http://site/dir/index.html}}, consectetur adipiscing elit,
```

in (La)TeX,

```
Lorem ipsum dolor [sit amet](http://site/dir/index.html), consectetur adipiscing elit,
```

in Markdown, and

```
Lorem ipsum dolor <a href="http://site/dir/index.html">sit amet</a>, consectetur adipiscing elit,
```

in html.


`` W ``{ ... }{ ... } is like `` L ``, but for a link to Wikipedia. The contents of the second capture field is supposed to be the part of the URL after `` https://en.wikipedia.org/wiki/ ``. Example:

```
W{Ann Arbor, Michigan}{Ann_Arbor,_Michigan}
```

[Ann Arbor, Michigan](https://en.wikipedia.org/wiki/Ann_Arbor,_Michigan)

### dict.txt

Is a file containing a dictionary that I use to construct prototype tables for procedures in my code. You will probably not need or want it, so just add a `` dict.txt `` containing the text "foo -> bar" or something like that (or just take the `` dict.txt `` from the repository). With some editing of the AWK scripts, the use for it can be removed. I still need it, so I'm not going to remove it myself.



