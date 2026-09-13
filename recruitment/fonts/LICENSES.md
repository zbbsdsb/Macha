# Embedded font licences

All fonts embedded in the recruitment PDFs are licensed under the **SIL Open Font
License 1.1**, which permits embedding and redistribution in documents.

| Family | Role in the document | Source | Licence |
|---|---|---|---|
| **Inter** (incl. Inter Display) | Latin body, headlines, all display typography | https://github.com/rsms/inter (v4.1) | SIL OFL 1.1 |
| **IBM Plex Mono** | Technical annotations, labels, diagram node names | https://github.com/IBM/plex | SIL OFL 1.1 |
| **Noto Sans SC** | Han text (Chinese edition) and CJK fallback | https://fonts.google.com/noto | SIL OFL 1.1 |

## How the files in `fonts/` were produced

`src/prepare_fonts.py` regenerates every file here:

- **Inter** ships as a 36-face TrueType Collection (`Inter.ttc`), which ReportLab
  cannot use directly. The nine faces the document needs are extracted into
  standalone TTFs. Inter Display faces are used at display sizes where the
  tighter optical spacing matters.
- **Noto Sans SC** ships as a variable font. The three weights used (400 / 500 /
  700) are instanced into statics so that weight — not axis interpolation —
  determines the rendering.
- **IBM Plex Mono** is taken as static TTFs from the Google Fonts mirror.

The subsetted font programs are embedded in the output with subset prefixes
(e.g. `AAAAAA+Inter-Regular`). No unembedded font is declared in either PDF.

## Why not system fonts

Using Microsoft YaHei or SimSun would avoid the download, but their licences do
not clearly permit embedding in a publicly distributed document. All three
families above are explicitly embeddable, which is why the build fetches them
rather than reading from the system font directory.
