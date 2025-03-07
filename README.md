# ANStoX

A set of AWK scripts to convert annotated source to code, tests, and documentation.


This method uses one or more `` .ans `` (ANNotated Source) files which are filtered through one of the AWK-language filters and mashed together to form a document. The idea is that each `` .ans `` file contains a number of code snippets, each with a short bit of documentation for it, and a number of test cases for it.


Examples:

```
awk -f anstocode.awk alpha.ans beta.ans >thefile.scm

awk -f anstotest.awk alpha.ans beta.ans >thefile.test

awk -f anstomd.awk dict.txt alpha.ans beta.ans >README.md

awk -f anstotex.awk dict.txt alpha.ans beta.ans >thedoc.tex
```

In these cases, `` alpha.ans `` and `` beta.ans `` are source files containing documentation tags, test tags, and code tags. The code tags are printed to the code file by `` anstocode.awk ``, the test tags to the test file by `` anstotest.awk ``, and the content of the documentation and code tags are printed in different ways to the readme document by `` anstomd.awk `` and to the thedoc document by `` anstotex.awk ``. The `` dict.txt `` file is a special case which will be explained below.

## Tags
### Documentation text

The `` MD `` tag used to be for documentation text. Example:

```
MD(
This is a short docu text.
MD)
```

You would start the block with `` MD `` and an open parenthesis in the leftmost column, then newline and text, newline again and `` MD `` and a closing parenthesis.


The contents of the `` MD `` tag was processed for styling and output by the `` anstomd.awk `` and `` anstotex.awk `` scripts.


Very recently I got tired of having text omitted because I had forgotten to place `` MD `` tags around it. So I changed the specification, and the processing, to let any text outside of `` CB `` and `` TT `` tags be documentation text. Just put empty lines before and after paragraphs, and in particular end the source file with an empty line (otherwise the last paragraph will vanish).

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

The contents of the `` CB `` tag is output without further processing by all the scripts except `` anstotest.awk ``. `` anstomd.awk `` and `` anstotex.awk `` add elements around the tag's output, suitable for presenting code (i.e. triple backticks for Markdown, the `` lstlisting `` environment for LaTeX).

### Verbatim

The `` VB `` tag is for text that should be output with no extra processing and presented with triple backticks for Markdown, and the `` verbatim `` environment for LaTeX. The contents of the tag aren't output by `` anstocode.awk `` or `` anstotest.awk ``.

### Test cases

The `` TT `` tag is used for test case code which will be output by `` anstotest.awk `` alone. The `` anstotest.awk `` script is geared towards the `` tcltest `` engine, but should be possible to convert to other test engines by editing the preamble and postamble in the script.

```
TT(
::tcltest::test foobar-1.0 {try the foobar} -body {
   ...
} -output "..."
TT)
```
### Pulled text

The `` PT `` tag is different. In no script is its contents output. Instead, one uses `` MD `` inside it to get the documentation scripts to output the text. The point of using is that it adds formatting around the text within it: for Markdown it is a preciding and a succeeding horizontal rule; for LaTeX it's the beginning and end of the `` pulledtext `` environment.

### Lists

The `` IT `` and `` EN `` tags _at the beginning of the line_ renders the line as a bulleted or a numbered list item, respectively.


Example:

```
IT fee
IT fie
IT foe
```
## Headings

The headings tags are the same as in html, `` H1 `` to `` H6 ``, only you put them at the start of the line, with the heading text following. They are translated to hash groups for Markdown, and to different heading elements for LaTeX.

```
H1 A title
```
### IG, EM and KB

These three beginning of the line tags:

1. import a graphics element (an image)
1. wrap the entire line in italics elements
1. wrap the entire line in keyboard font elements
```
IG /images/myimage.png

EM This line will be in italics
```
### IF, IX, NI

These tags are mostly useful for translation to LaTeX.


`` IF `` imports an image, but puts it in a float and adds a caption.

```
IF /images/myimage.png Look how pretty
```

`` IX `` makes an index entry from the text that follows it. `` NI `` puts a `` \noindent `` in front of the line.

## Styling
### Appearance

`` B ``{ ... } renders text bold. `` E ``{ ... } renders text in italics. `` K ``{ ... } renders text in keyboard font.

### Links, footnotes, and references

`` F ``{ ... } creates a LaTeX footnote, or just a parenthesized bit of text in Markdown. `` R ``{ ... }{ ... } inserts a page reference text in LaTeX and a link in Markdown.

```
Lorem ipsum dolor R{sit amet}{toc-label}, consectetur adipiscing elit,
```

Is rendered

```
Lorem ipsum dolor sit amet (see page \pageref{toc-label}), consectetur adipiscing elit,
```

in LaTeX, and

```
Lorem ipsum dolor [sit amet](https://github.com/hoodiecrow/ConsTcl#toc-label), consectetur adipiscing elit,
```

in Markdown (clearly some personalizing is necessary).


`` S ``{ ... }{ ... } is the same as `` R ``, but adds elements for keyboard font around the anchor.


`` L ``{ ... }{ ... } is like `` R ``, but for an external link.

```
Lorem ipsum dolor L{sit amet}{http://site/dir/index.html}, consectetur adipiscing elit,
```

Is rendered

```
Lorem ipsum dolor sit amet\footnote{See \texttt{http://site/dir/index.html}}, consectetur adipiscing elit,
```

in LaTeX, and

```
Lorem ipsum dolor [sit amet](http://site/dir/index.html), consectetur adipiscing elit,
```

in Markdown.


`` W ``{ ... }{ ... } is like `` L ``, but for a link to Wikipedia. The contents of the second capture field is supposed to be the part of the URL after `` https://en.wikipedia.org/wiki/ ``.

### dict.txt

Is a file containing a dictionary that I use to construct prototype tables for procedures in my code. You will probably not need or want it, so just add a `` dict.txt `` containing the text "foo -> bar" or something like that (or just take the `` dict.txt `` from the repository). With some editing of the AWK scripts, the use for it can be removed. I still need it, so I'm not going to remove it myself.



