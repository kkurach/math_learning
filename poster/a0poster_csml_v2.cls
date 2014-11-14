%% Poster style  
%% 
%% This is a new version of the mpi poster style which now also 
%% works with pdflatex. 
%% 
%% 
%% see example poster for how to use it
%% 
%% the original file was from 
%% http://www.physik.uni-augsburg.de/theo3/Comp/hp750c/computing_hp750c_A0.de.shtml
%% 

\ProvidesClass{a0poster_mpi_v2}
\NeedsTeXFormat{LaTeX2e}[1995/06/01]
\LoadClass{article}

\newif\ifportrait
\newif\ifanullb
\newif\ifanull
\newif\ifaeins
\newif\ifazwei
\newif\ifadrei
\newif\ifdraft

\newcount\xkoord
\newcount\ykoord
\newcount\xscale
\newcount\yscale

\DeclareOption{a0b}{
\anullbtrue
\xkoord=2594 % big points (1 bp=1/72 inch)
\ykoord=3370 % big points (1 bp=1/72 inch)
\xscale=2
\yscale=2
}
\DeclareOption{a0}{
\anulltrue\anullbfalse
\xkoord=2380 % big points (1 bp=1/72 inch)
\ykoord=3368 % big points (1 bp=1/72 inch)
\xscale=2
\yscale=2
}
\DeclareOption{a1}{
\aeinstrue\anullbfalse
\xkoord=1684 % big points (1 bp=1/72 inch)
\ykoord=2380 % big points (1 bp=1/72 inch)
\xscale=3
\yscale=3
}
\DeclareOption{a2}{
\azweitrue\anullbfalse
\xkoord=1190 % big points (1 bp=1/72 inch)
\ykoord=1684 % big points (1 bp=1/72 inch)
\xscale=4
\yscale=4

}
\DeclareOption{a3}{
\adreitrue\anullbfalse
\xkoord=842  % big points (1 bp=1/72 inch)
\ykoord=1190 % big points (1 bp=1/72 inch)
\xscale=6
\yscale=6
}
\DeclareOption{landscape}{
\portraitfalse
}
\DeclareOption{portrait}{
\portraittrue
}
\DeclareOption{draft}{
\drafttrue
}
\DeclareOption{final}{
\draftfalse
}
\DeclareOption*{\PackageWarning{a0poster}{Unknown Option \CurrentOption}}
\ExecuteOptions{landscape,a0b,final}
\ProcessOptions\relax

\ifanullb
   \setlength{\paperwidth}{119cm}
   \setlength{\paperheight}{88cm}
   \setlength{\textwidth}{116cm}
   \setlength{\textheight}{88cm}
\else\ifanull
        \setlength{\paperwidth}{118.82cm}
        \setlength{\paperheight}{83.96cm}
        \setlength{\textwidth}{117.82cm}
        \setlength{\textheight}{82.96cm}
     \else\ifaeins
             \setlength{\paperwidth}{83.96cm}
             \setlength{\paperheight}{59.4cm}
             \setlength{\textwidth}{83.96cm}
             \setlength{\textheight}{58.4cm}
          \else\ifazwei
                  \setlength{\paperwidth}{59.4cm}
                  \setlength{\paperheight}{41.98cm}
                  \setlength{\textwidth}{58.4cm}
                  \setlength{\textheight}{40.98cm}
               \else\ifadrei
                       \setlength{\paperwidth}{41.98cm}
                       \setlength{\paperheight}{29.7cm}
                       \setlength{\textwidth}{40.98cm}
                       \setlength{\textheight}{28.7cm}
                    \else\relax
                    \fi
               \fi
          \fi
     \fi
\fi


\ifportrait
   \newdimen\tausch
   \setlength{\tausch}{\paperwidth}
   \setlength{\paperwidth}{\paperheight}
   \setlength{\paperheight}{\tausch}
   \setlength{\tausch}{\textwidth}
   \setlength{\textwidth}{\textheight}
   \setlength{\textheight}{\tausch}
\else\relax
\fi

%% Setting proper dimensions for a DIN A0 printer

\setlength{\headheight}{0 cm}
\setlength{\headsep}{0 cm}
\setlength{\topmargin}{-10.7 mm}  % -1in +1.47cm
\setlength{\oddsidemargin}{-21.4 mm} % -1in +0.4cm

\input{a0size.sty}

\renewcommand{\tiny}{\fontsize{12}{14}\selectfont}
\renewcommand{\scriptsize}{\fontsize{14.4}{18}\selectfont}   
\renewcommand{\footnotesize}{\fontsize{17.28}{22}\selectfont}
\renewcommand{\small}{\fontsize{20.74}{25}\selectfont}
\renewcommand{\normalsize}{\fontsize{24.88}{30}\selectfont}
\renewcommand{\large}{\fontsize{29.86}{37}\selectfont}
\renewcommand{\Large}{\fontsize{35.83}{45}\selectfont}
\renewcommand{\LARGE}{\fontsize{43}{54}\selectfont}
\renewcommand{\huge}{\fontsize{51.6}{64}\selectfont}
\renewcommand{\Huge}{\fontsize{61.92}{77}\selectfont}
\newcommand{\veryHuge}{\fontsize{74.3}{93}\selectfont}
\newcommand{\VeryHuge}{\fontsize{89.16}{112}\selectfont}
\newcommand{\VERYHuge}{\fontsize{107}{134}\selectfont}
\renewcommand{\section}{\@startsection {section}{1}{\z@}%
  {-3.5ex \@plus -1ex \@minus -.2ex}%
  {2.3ex \@plus.2ex}%
  {\reset@font\Large\bfseries\sffamily}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
  {-3.25ex\@plus -1ex \@minus -.2ex}%
  {1.5ex \@plus .2ex}%
  {\reset@font\large\bfseries\sffamily}}

\setlength\smallskipamount{6pt plus 2pt minus 2pt}
\setlength\medskipamount{12pt plus 4pt minus 4pt}
\setlength\bigskipamount{24pt plus 8pt minus 8pt}

\setlength\abovecaptionskip{25pt}
\setlength\belowcaptionskip{0pt}
\setlength\abovedisplayskip{25pt plus 6pt minus 15 pt}
\setlength\abovedisplayshortskip{0pt plus 6pt}
\setlength\belowdisplayshortskip{13pt plus 7pt minus 6pt}
\setlength\belowdisplayskip\abovedisplayskip

\normalsize


\AtBeginDocument{
\ifanullb
   \ifportrait\special{papersize=91.51cm,120cm}\else\special{papersize=120cm,91.51cm}\fi
\else\ifanull
        \ifportrait\special{papersize=83.96cm,118.82cm}\else\special{papersize=118.82cm,83.96cm}\fi
     \else\ifaeins
             \ifportrait\special{papersize=59.4cm,83.96cm}\else\special{papersize=83.96cm,59.4cm}\fi
          \else\ifazwei
                  \ifportrait\special{papersize=41.98cm,59.4cm}\else\special{papersize=59.4cm,41.98cm}\fi
               \else\ifadrei
                      \ifdraft
                       \ifportrait\special{papersize=29.7cm,41.35cm}\else\special{papersize=41.98cm,29.0cm}\fi
                      \else
                       \ifportrait\special{papersize=29.7cm,41.98cm}\else\special{papersize=41.98cm,29.7cm}\fi
                      \fi
                    \else\relax
                    \fi
               \fi
          \fi
     \fi
\fi
\pagestyle{empty}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Headers - general definitions for all of them -  by Ule
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% I use saveboxes here because then the user can not only define the
% text but also its size or font. 
\newsavebox{\PosterTitle}
\newsavebox{\PosterAuthor}
\newsavebox{\PosterAddress}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header without logo            - by Ule      %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%




\newcommand{\headerNoLogo}{
\vspace{1cm}%
\hfill%
\begin{minipage}{0.9\textwidth} %authors and addresses:
\begin{center}
\raisebox{1.5cm}{\usebox{\PosterTitle}}\\
\raisebox{0cm}{\usebox{\PosterAuthor}}\\
\raisebox{-1.5cm}{\usebox{\PosterAddress}}
\hspace{1cm}
\end{center}
\end{minipage}
\hfill%
\vspace{3cm}%
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header with custom logo             - by Ule      %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\headerCustomLogo}{
\vspace{1cm}%
%
\hfill
\begin{minipage}{0.1\textwidth}
\includegraphics[width=\textwidth]{\LeftLogoFile}
\end{minipage}
\hfill%
\begin{minipage}{0.7\textwidth} %authors and addresses:
\begin{center}
\raisebox{1.5cm}{\usebox{\PosterTitle}}\\
\raisebox{0cm}{\usebox{\PosterAuthor}}\\
\raisebox{-1.5cm}{\usebox{\PosterAddress}}
\hspace{1cm}
\end{center}
\end{minipage}
\hfill%
\begin{minipage}{0.1\textwidth}
\includegraphics[width=\textwidth]{\RightLogoFile}
\end{minipage}
\hfill%
%
\vspace{3cm}%
}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header with MPI logo             - by Ule      %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\headerMpi}{%
\newcommand{\LeftLogoFile}{csml_logo_vector2}
\newcommand{\RightLogoFile}{csml_logo_vector2}
\headerCustomLogo
}





%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Poster                        %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newsavebox{\dummybox}
\newsavebox{\spalten}

\newenvironment{poster} {
   \vfill \begin{minipage}{\textwidth}  }
  {\end{minipage} \vfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                PosterColumn                       %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\columnfrac}{.3}
\newenvironment{PosterColumn}{%
  \hfill\begin{minipage}[t]{\columnfrac\textwidth}}{\end{minipage}\hfill%
}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%               PosterBox - does not require ps output - by Ule
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newcommand{\PosterBox}[1]{{%
\setlength{\fboxsep}{8mm}
\setlength{\fboxrule}{2pt}
\mbox{}\\
\framebox[\textwidth][l]{\parbox{0.95\textwidth}{\bf\Large \textsf{#1}}}\\[1cm]
}}

\newcommand{\PosterBoxSmall}[1]{{%
\setlength{\fboxsep}{8mm}
\setlength{\fboxrule}{2pt}
\mbox{}\\
\framebox[\textwidth][l]{\parbox{0.95\textwidth}{#1}}\\[1cm]
}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                Header                        %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%\newenvironment{header}[1][1. 1. 1.] {
%%    \vspace{2em}
    
%%    \begin{center}
%%    \newrgbcolor{hcolor}{#1}
%%    \begin{lrbox}{\dummybox} 
%%    \begin{minipage}[t]{.9\textwidth}
%% }   
%% {  \end{minipage} \end{lrbox}
%%      \raisebox{-\depth}{\hspace{.5in}\hspace{-4mm}
%%       \psshadowbox[fillstyle=solid,fillcolor=hcolor,framesep=8mm]
%%        {\usebox{\dummybox}}} \end{center}
%%     \vspace{2em}
%% }



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%               Hintergrund                    %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%\newcommand{\background}[3]{\newrgbcolor{cgradbegin}{#1}
%%  \newrgbcolor{cgradend}{#2} 
%%  \psframe[fillstyle=gradient,gradend=cgradend,
%%  gradbegin=cgradbegin,gradmidpoint=#3](0.,0.)(1.\textwidth,-1.\textheight)}



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%                Header no frame        - by Ule               %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%\newenvironment{headernf}[1][1. 1. 1.] {
%%    \vspace{2em}
    
%%    \begin{center}
%%    \newrgbcolor{hcolor}{#1}
%%    \begin{lrbox}{\dummybox} 
%%    \begin{minipage}[t]{.9\textwidth}
%% }   
%% {  \end{minipage} \end{lrbox}
%%      \raisebox{-\depth}{\hspace{.5in}\hspace{-4mm}
%%%       \psshadowbox[fillstyle=solid,fillcolor=hcolor,framesep=8mm]
%%        {\usebox{\dummybox}}} \end{center}
%%     \vspace{2em}
%% }



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%                Header no shadow              %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%\newenvironment{headerns}[1][1. 1. 1.] {
%%    \vspace{2em}
    
%%    \begin{center}
%%    \newrgbcolor{hcolor}{#1}
%%    \begin{lrbox}{\dummybox} 
%%    \begin{minipage}[t]{.9\textwidth}
%% }   
%% {  \end{minipage} \end{lrbox}
%%      \raisebox{-\depth}{\hspace{.5in}\hspace{-4mm}
%%       \psshadowbox[fillstyle=solid,fillcolor=hcolor,framesep=8mm,shadowsize=0pt]
%%    {\usebox{\dummybox}}} \end{center}
%%     \vspace{2em}
%% }




%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                pbox                          %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%\newenvironment{pbox}[1][1. 1. 1.] {
%%   \newrgbcolor{bcolor}{#1}
%%  \begin{lrbox}{\dummybox}%
%%    \begin{minipage}{0.96\linewidth}}%
%%    {\end{minipage}
%%  \end{lrbox}
%%  \raisebox{-\depth}{\hspace{-.5em} 
%%   \psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=1em]{\usebox{\dummybox}}} \vspace{1em} \vfill}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%                pbox   no shadow              %%%             
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%\newenvironment{pboxns}[1][1. 1. 1.] {
%%   \newrgbcolor{bcolor}{#1}
%%  \begin{lrbox}{\dummybox}%
%%    \begin{minipage}{0.96\linewidth}}%
%%    {\end{minipage}
%%  \end{lrbox}
%%  \raisebox{-\depth}{\hspace{-.5em} 
%%   \psshadowbox[fillstyle=solid,fillcolor=bcolor,framesep=1em,shadowsize=0pt]{\usebox{\dummybox}}} \vspace{1em} \vfill}





\endinput
%% 
%% End of file `a0poster.cls'.





