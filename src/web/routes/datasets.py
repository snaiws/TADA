from flask import Blueprint, render_template, request



datasets_bp = Blueprint('datasets', __name__)


# Dataset 리스트
@datasets_bp.route('/', methods=['GET'])
def list_datasets():
    # 데이터셋 리스트
    datasets = None
    # datasets = Dataset.query.all()  # DB 쿼리###################
    return render_template('datasets.html', datasets=datasets)


# Dataset 상세 페이지
@datasets_bp.route('/<dataset_type>', methods=['GET'])
def dataset_detail(dataset_type):
    dataset = Dataset.query.filter_by(type=dataset_type).first()
    if not dataset:
        return "Dataset not found", 404
    return render_template('detail.html', dataset=dataset)