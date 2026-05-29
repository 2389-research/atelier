import fs from 'fs';
import { topWords, stats } from './wordfreq.js';

const [, , filePath, nArg] = process.argv;

if (!filePath) {
  console.error('Usage: node src/cli.js <file> [n]');
  process.exit(1);
}

const n = nArg ? parseInt(nArg, 10) : 10;

try {
  const text = fs.readFileSync(filePath, 'utf-8');

  const top = topWords(text, n);
  const { total, unique } = stats(text);

  console.log('Top words:');
  top.forEach(({ word, count }) => {
    console.log(`  ${word}: ${count}`);
  });

  console.log(`\nStats: ${total} total, ${unique} unique`);
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error(`Error: File not found: ${filePath}`);
  } else {
    console.error(`Error: ${error.message}`);
  }
  process.exit(1);
}
