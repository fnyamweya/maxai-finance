
from __future__ import annotations
import argparse, os, shutil, json, joblib
from huggingface_hub import HfApi, create_repo, upload_folder

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--model_dir', required=True, help='Directory with cash_model.joblib')
    ap.add_argument('--repo', required=True, help='hub repo like username/maxai-finance-cash')
    ap.add_argument('--private', action='store_true', help='Create as private repo')
    args = ap.parse_args()

    if not os.path.exists(os.path.join(args.model_dir, 'cash_model.joblib')):
        raise SystemExit("cash_model.joblib not found in model_dir")

    # create a temp export folder
    export_dir = 'hf_export'
    if os.path.exists(export_dir):
        shutil.rmtree(export_dir)
    os.makedirs(export_dir, exist_ok=True)
    shutil.copy(os.path.join(args.model_dir, 'cash_model.joblib'), os.path.join(export_dir, 'cash_model.joblib'))
    # minimal model card & config
    with open(os.path.join(export_dir, 'README.md'),'w') as f:
        f.write('# maxAI Finance — Cashflow Forecaster\nSee the money before it moves.')
    with open(os.path.join(export_dir, 'config.json'),'w') as f:
        json.dump({'task':'time-series-forecasting','quantiles':[0.1,0.5,0.9],'framework':'scikit-learn'}, f)

    api = HfApi()
    try:
        create_repo(args.repo, private=args.private, exist_ok=True)
    except Exception as e:
        print('Repo exists or cannot create:', e)
    upload_folder(repo_id=args.repo, folder_path=export_dir, commit_message='Add maxAI cash model')
    print('Uploaded to', args.repo)

if __name__ == '__main__':
    main()
