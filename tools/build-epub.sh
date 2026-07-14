#!/usr/bin/env bash
# build-epub.sh — Build Kindle-compatible EPUB3 of Building Autonomous Robots From Scratch
# Idempotent: safe to re-run after chapter edits.
#
# Content decisions:
#   - Philosophy page is SKIPPED (it reads as meta-commentary on the site, not book content).
#   - Home and Roadmap are skipped (navigation-only pages).
#   - Parts I–VI are inserted as level-1 headings so the EPUB TOC nests Part → Chapter.
#   - Each chapter's "## Try It" iframe is replaced with a static screenshot image + caption.
#   - "Continue →" nav links are stripped.
#
# Outputs:
#   /book/cover.png
#   /book/building-autonomous-robots.epub

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "${SCRIPT_DIR}/.." && pwd)"
BOOK_DIR="${REPO}/book"
TOOLS_DIR="${REPO}/tools"
TMPDIR="${REPO}/.epub-tmp"
EPUB_OUT="${BOOK_DIR}/building-autonomous-robots.epub"
COVER="${BOOK_DIR}/cover.png"

mkdir -p "${BOOK_DIR}" "${TMPDIR}"

echo "=== Step 1: Generate cover ==="
if [ -f "${COVER}" ]; then
  echo "  cover.png already exists, skipping playwright render."
else
  echo "  Running playwright to render cover..."
  node "${TOOLS_DIR}/make_cover.js" "${COVER}"
  echo "  Cover generated: ${COVER}"
fi

echo ""
echo "=== Step 2: Preprocess chapters ==="
python3 "${TOOLS_DIR}/preprocess_chapters.py" "${REPO}" "${TMPDIR}"

echo ""
echo "=== Step 3: Build EPUB with pandoc ==="

# Read spine order from spine.txt
SPINE_FILE="${TMPDIR}/spine.txt"
if [ ! -f "${SPINE_FILE}" ]; then
  echo "ERROR: spine.txt not found after preprocessing." >&2
  exit 1
fi

# Build pandoc input file list from spine (compatible with bash 3.2)
INPUT_FILES=()
while IFS= read -r line; do
  INPUT_FILES+=("$line")
done < "${SPINE_FILE}"

# Metadata
BOOK_DATE="$(date +%Y-%m-%d)"

# Resource paths: pandoc needs to find images relative to where they're referenced.
# The preprocessed markdown references: assets/sim-screenshots/chapterNN.png
# We set resource-path to REPO so pandoc looks there.
pandoc \
  "${INPUT_FILES[@]}" \
  --to epub3 \
  --output "${EPUB_OUT}" \
  --metadata title="Building Autonomous Robots From Scratch" \
  --metadata author="Ishmum Jawad Khan" \
  --metadata lang=en \
  --metadata date="${BOOK_DATE}" \
  --metadata description="A discovery-driven course in building autonomous robots, from motors and wheels to full autonomous flight stacks." \
  --toc \
  --toc-depth=2 \
  --epub-cover-image="${COVER}" \
  --resource-path="${REPO}:${TMPDIR}" \
  --split-level=2 \
  2>&1

echo ""
echo "=== Step 4: Verify ==="

# pandoc exit code already checked by set -e
echo "  pandoc: OK (exit 0)"

# File size
SIZE=$(du -sh "${EPUB_OUT}" | cut -f1)
echo "  EPUB size: ${SIZE}"
BYTES=$(wc -c < "${EPUB_OUT}")
if [ "${BYTES}" -lt 1000000 ]; then
  echo "  WARNING: EPUB is smaller than 1 MB (${BYTES} bytes) — images may be missing." >&2
else
  echo "  Size check: OK (${BYTES} bytes)"
fi

# Pandoc renames images to file1.png, file2.png, etc. inside EPUB/media/.
# Spot-check: verify the expected number of chapter images are present (45 chapters + cover).
echo "  Checking image presence in EPUB..."
IMAGE_COUNT=$(unzip -l "${EPUB_OUT}" | grep -c "EPUB/media/file.*\.png" || true)
echo "    Chapter + cover images in EPUB/media/: ${IMAGE_COUNT} (expected 46)"
if [ "${IMAGE_COUNT}" -lt 45 ]; then
  echo "    WARNING: Fewer than 45 images found — some screenshots may be missing!" >&2
else
  echo "    Image check: OK"
fi

# Quick spot-check: print first, middle, last file entries
FIRST=$(unzip -l "${EPUB_OUT}" | grep "EPUB/media/file" | head -1 | awk '{print $NF}')
LAST=$(unzip -l "${EPUB_OUT}" | grep "EPUB/media/file" | tail -1 | awk '{print $NF}')
echo "    First image: ${FIRST}"
echo "    Last image:  ${LAST}"

# Check content files exist
CONTENT_COUNT=$(unzip -l "${EPUB_OUT}" | grep -c "\.xhtml\|\.html" || true)
echo "  Content files (.xhtml/.html): ${CONTENT_COUNT}"

echo ""
echo "=== Build complete ==="
echo "  EPUB: ${EPUB_OUT}"
echo "  Size: ${SIZE}"
