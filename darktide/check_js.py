import pathlib, sys
sys.stdout.reconfigure(encoding='utf-8')
d = pathlib.Path('C:/Users/iamgo/.openclaw/workspace/darktide/output/index.html').read_bytes()
idx = d.find(b'MEMBER_NAMES:')
if idx >= 0:
    chunk = d[idx:idx+200].decode('utf-8', errors='replace')
    print('MEMBER_NAMES:', chunk[:150])
idx2 = d.find(b'JOBS:')
if idx2 >= 0:
    before = d[idx2-20:idx2].decode('utf-8', errors='replace')
    chunk2 = d[idx2:idx2+300].decode('utf-8', errors='replace')
    print('Before JOBS:', repr(before))
    print('JOBS:', chunk2[:250])
# Check if CONFIG closes properly after DISBAND
end_idx = d.find(b'DISBAND_REFUND')
if end_idx >= 0:
    end_chunk = d[end_idx:end_idx+40]
    print('After DISBAND:', repr(end_chunk))
