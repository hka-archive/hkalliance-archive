# Hong Kong Alliance Website Archive · 香港支聯會網站存檔

[![Health check](https://github.com/OWNER/hkalliance-archive/actions/workflows/healthcheck.yml/badge.svg)](https://github.com/OWNER/hkalliance-archive/actions/workflows/healthcheck.yml)

**https://hkalliance-archive.org/**

An archive of **hka8964.wordpress.com**, the website of the Hong Kong Alliance in Support of Patriotic
Democratic Movements of China (香港市民支援愛國民主運動聯合會, 香港支聯會). It holds 372 posts and 46 pages
from 2012 to 2021: statements, event records, news and photographs. The website went offline when the
Alliance disbanded in September 2021. It was saved shortly before that, and is presented here as it was.

本網站存檔收錄香港市民支援愛國民主運動聯合會（香港支聯會）網站 hka8964.wordpress.com 於 2012 至 2021 年間的
372 篇文章及 46 個頁面，包括聲明、活動紀錄、新聞及照片。網站於 2021 年 9 月支聯會解散時下線，在此之前已被保存，
現按原貌呈現。

## Purpose 目的

To keep this part of Hong Kong's history available to readers, researchers and journalists, in its
original form and with its original dates.

讓讀者、研究人員及記者能繼續查閱這段香港歷史，並保留其原有內容及日期。

- **Not run by the Alliance.** This archive is not run by, and does not speak for, the Hong Kong Alliance or
  any of its former members. 本存檔並非由支聯會或其前成員營運，亦不代表他們。
- **Please do not send money.** The Alliance's bank accounts and donation details have been removed from the
  archive, because the organisation no longer exists. 支聯會已解散，存檔已移除其銀行戶口及捐款資料，請勿捐款。
- **Every page links to its original capture** on the Wayback Machine, so its content can be checked
  independently. 每一頁均附有 Wayback Machine 原頁存檔連結，方便獨立核實。
- **No tracking.** The archive uses no analytics, tracking scripts or cookies. 本存檔不使用任何分析、追蹤程式或 cookies。

## Catalogue 文章目錄

[`catalogue/`](catalogue/) lists all 372 posts and 46 pages, with their date, title, categories, tags, a
link to each one in the archive, its original address and a Wayback Machine link. It also counts the
posts by year and by category.

[`catalogue/`](catalogue/) 列出全部 372 篇文章及 46 個頁面，包括日期、標題、分類、標籤、存檔連結、原網址及
Wayback Machine 連結，並按年份及分類統計文章數目。

- [`posts.csv`](catalogue/posts.csv): opens in Excel, Numbers or Google Sheets 可用 Excel、Numbers 或 Google 試算表開啟
- [`posts.json`](catalogue/posts.json): the same data for programs 供程式使用的相同資料

The same files are published on the archive at https://hkalliance-archive.org/catalogue/.
同一目錄亦在存檔網站 https://hkalliance-archive.org/catalogue/ 提供。

## Report a problem 回報問題

| What | Where |
|---|---|
| A page doesn't load, a link or image is broken, or text displays wrongly<br>網頁無法開啟、連結或圖片失效、文字顯示錯誤 | [Open an issue 開立問題回報](../../issues/new/choose) (public) |
| A correction, a removal request, a copyright concern, or anything personal or sensitive<br>更正、移除要求、版權問題，或任何涉及個人或敏感資料的事宜 | Email **info@hkalliance-archive.org** (private) |
| A security problem with the website<br>網站保安問題 | See [SECURITY.md](SECURITY.md) |

Issues on GitHub are public. Please don't include names, contact details or other personal information
in them. GitHub 上的問題回報是公開的，請勿填寫姓名、聯絡方式或其他個人資料。

## Status 運作狀態

The archive is checked automatically every Monday. The badge at the top shows the latest result. If a
check fails, an issue titled **"Health check failed"** opens here automatically, and is closed when the
archive is working again.

系統每星期一自動檢查存檔，頂部標誌顯示最新結果。如檢查失敗，本頁會自動開立名為「Health check failed」的問題回報，
恢復正常後自動關閉。

The check confirms that:
- the home page and a random sample of posts load, show the archive notice and display Chinese text correctly
- addresses with and without a final `/` both work, and missing pages show the archive's "page not found" page
- the article list (`catalogue/posts.json`), `robots.txt` and `llms.txt` are available
- the removed donation details have not reappeared
- the HTTPS certificate and the domain registration are not close to expiry

The check is [`tools/healthcheck.py`](tools/healthcheck.py). Anyone can run it:
`python3 tools/healthcheck.py https://hkalliance-archive.org/` (Python 3.9 or later, no other software).

## Copyright 版權

The archived content belongs to its original authors: the Hong Kong Alliance in Support of Patriotic
Democratic Movements of China, and the photographers and organisations credited in the posts. It is
preserved for the historical record. If you hold rights in any of the content and want it corrected or
removed, email **info@hkalliance-archive.org**.

存檔內容版權屬原作者所有，包括香港市民支援愛國民主運動聯合會，以及文章所註明的攝影師及機構。本存檔保存這些內容作歷史記錄之用。
如你擁有任何內容的權利並希望更正或移除，請電郵 **info@hkalliance-archive.org**。

The code in this repository (the health check) is released under the [MIT License](LICENSE). The
catalogue lists the archived posts; the posts and photographs themselves are not part of this repository.
