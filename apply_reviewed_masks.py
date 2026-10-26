"""Apply masks downloaded by HUMAN_REVIEW_TOOL.html and export matching YOLO polygons."""
import argparse,csv,json,shutil
from pathlib import Path
import cv2

def main():
 p=argparse.ArgumentParser();p.add_argument('--dataset',default='.');p.add_argument('--review-masks',required=True,help='Folder containing corrected <image_id>_mask.png files downloaded from browser review tool');p.add_argument('--audit-json',required=True);p.add_argument('--apply',action='store_true',help='Actually copy masks/update labels/manifest; without this flag performs validation only');a=p.parse_args();root=Path(a.dataset);corr=Path(a.review_masks);audit=json.loads(Path(a.audit_json).read_text(encoding='utf-8'));dec=audit.get('decisions',[]);approved={d['image_id']:d for d in dec if d.get('status') in ('approved','corrected') and d.get('reviewer')};rows=list(csv.DictReader((root/'manifest.csv').open(encoding='utf-8')));errors=[];todo=[]
 for r in rows:
  image_id=r['image_id'];d=approved.get(image_id)
  if not d:continue
  if d.get('status')=='corrected':
   src=corr/(image_id+'_mask.png')
   if not src.is_file():errors.append(f'{image_id}: audit says corrected but mask file is missing');continue
   dst=root/r['mask_path'];m=cv2.imread(str(src),cv2.IMREAD_GRAYSCALE);im=cv2.imread(str(root/r['local_image']))
   if m is None or im is None or m.shape[:2]!=im.shape[:2]:errors.append(f'{image_id}: mask/image sizes mismatch');continue
   todo.append((r,d,src,dst,m))
  else:todo.append((r,d,None,None,None))
 print(f'Audit decisions accepted/corrected: {len(approved)}; corrections requiring mask files: {sum(d.get("status")=="corrected" for d in approved.values())}; actionable rows: {len(todo)}')
 if errors:print('\n'.join(errors[:30]));raise SystemExit(2)
 if not a.apply:print('DRY RUN only. Review paths and rerun with --apply to update.');return
 backup=root/'human_review_backups';backup.mkdir(exist_ok=True)
 for r,d,src,dst,m in todo:
  if d.get('status')=='corrected':
   b=backup/r['mask_path'];b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dst,b);shutil.copy2(src,dst)
   # YOLO polygons trace external mask contours; standard YOLO polygons cannot express holes inside a contour.
   cs,_=cv2.findContours(m,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE);lines=[];h,w=m.shape[:2]
   for c in sorted(cs,key=cv2.contourArea,reverse=True):
    if cv2.contourArea(c)<3:continue
    c=cv2.approxPolyDP(c,max(.8,.0015*cv2.arcLength(c,True)),True).reshape(-1,2)
    if len(c)<3:continue
    vals=[]
    for x,y in c:vals.extend([min(1,max(0,float(x)/max(1,w-1))),min(1,max(0,float(y)/max(1,h-1)))])
    lines.append('0 '+' '.join(f'{v:.6f}' for v in vals))
   lp=root/r['label_path'];lp.write_text('\n'.join(lines)+('\n' if lines else ''),encoding='utf-8')
  r['annotation_status']='HUMAN_VERIFIED_'+('CORRECTED' if d.get('status')=='corrected' else 'ACCEPTED_PRELABEL');r['reviewer']=d.get('reviewer','');r['reviewed_at']=d.get('time','')
 fields=list(dict.fromkeys(k for r in rows for k in r.keys()))
 with (root/'manifest.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
 print(f'Applied human review records to {len(todo)} rows. Backups for corrected masks: {backup}. Re-run the dataset validation before training.')
if __name__=='__main__':main()
