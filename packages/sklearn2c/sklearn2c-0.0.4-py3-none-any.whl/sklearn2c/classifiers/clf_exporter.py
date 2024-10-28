import numpy as np
from ..generic_exporter import GenericExporter, np2str

class BayesExporter(GenericExporter):
    def __init__(self, bayes_classifier) -> None:
        super().__init__()
        self.clf = bayes_classifier
        self.num_classes = len(self.clf.classes)

    def create_header(self):
        super().create_header()
        self.header_str += f"#define NUM_CLASSES {self.num_classes}\n"
        self.header_str += f"#define NUM_FEATURES {self.clf.num_features}\n"
        self.header_str += f"#define CASE {self.clf.case}\n"
        self.header_str += "extern float MEANS[NUM_CLASSES][NUM_FEATURES];\n"
        self.header_str += "extern const float CLASS_PRIORS[NUM_CLASSES];\n"
        if self.clf.case == 1:
            self.header_str += "extern const float sigma_sq;\n"
        elif self.clf.case ==  2:
            self.header_str += "extern const float INV_COV[NUM_FEATURES][NUM_FEATURES];\n"
        else:
            self.header_str += "extern const float INV_COVS[NUM_CLASSES][NUM_FEATURES][NUM_FEATURES];\n"
            self.header_str += "extern const float DETS[NUM_CLASSES];\n"
        self.header_str += '#endif\n'
    
    def create_source(self):
        super().create_source()
        self.source_str += f'float MEANS[NUM_CLASSES][NUM_FEATURES] = {np2str(self.clf.means)};\n'
        self.source_str += f'const float CLASS_PRIORS[NUM_CLASSES] = {np2str(self.clf.priors)};\n'
        if self.clf.case == 1:
            self.source_str += f'const float sigma_sq = {self.clf.sigma_sq};\n'
        elif self.clf.case == 2:
            self.source_str += f'const float INV_COV[NUM_FEATURES][NUM_FEATURES] = {np2str(self.clf.inv_cov)};\n'
        elif self.clf.case == 3: 
            self.source_str += f'const float INV_COVS[NUM_CLASSES][NUM_FEATURES][NUM_FEATURES] = {np2str(self.clf.inv_covs)};\n'
            self.source_str += f'const float DETS[NUM_CLASSES] = {np2str(self.clf.dets)};\n'
    
class DTClassifierExporter(GenericExporter):
    def __init__(self, dt_classifier) -> None:
        self.clf = dt_classifier
        super().__init__()
        self.tree = dt_classifier.tree_
        self.values = np.squeeze(self.tree.value).astype(int)

    def create_header(self):
        super().create_header()
        self.header_str += f"#define NUM_NODES {self.tree.node_count}\n"
        self.header_str += f"#define NUM_FEATURES {self.clf.n_features_in_}\n"
        self.header_str += f"#define NUM_CLASSES {len(self.clf.classes_)}\n"
        self.header_str += "extern const int LEFT_CHILDREN[NUM_NODES];\n"
        self.header_str += "extern const int RIGHT_CHILDREN[NUM_NODES];\n"
        self.header_str += "extern const int SPLIT_FEATURE[NUM_NODES];\n"
        self.header_str += "extern const float THRESHOLDS[NUM_NODES];\n"
        self.header_str += "extern const int VALUES[NUM_NODES][NUM_CLASSES];\n"
        self.header_str += '#endif\n'

    def create_source(self):
        super().create_source()
        self.source_str += f"const int LEFT_CHILDREN[NUM_NODES] = {np2str(self.tree.children_left)};\n"
        self.source_str += f"const int RIGHT_CHILDREN[NUM_NODES] = {np2str(self.tree.children_right)} ;\n"
        self.source_str += f"const int SPLIT_FEATURE[NUM_NODES] = {np2str(self.tree.feature)};\n"
        self.source_str += f"const float THRESHOLDS[NUM_NODES] = {np2str(self.tree.threshold)};\n"
        self.source_str += f"const int VALUES[NUM_NODES][NUM_CLASSES] = {np2str(self.values)};\n"
    

class KNNExporter(GenericExporter):
    def __init__(self, knn_classifier) -> None:
        self.clf = knn_classifier
        super().__init__()

    
    def create_header(self):
        super().create_header()
        self.header_str += f'#define NUM_CLASSES {len(self.clf.classes_)}\n'
        self.header_str += f'#define NUM_NEIGHBORS {self.clf.n_neighbors}\n'
        self.header_str += f'#define NUM_FEATURES {self.clf.n_features_in_}\n'
        self.header_str += f'#define NUM_SAMPLES {self.clf.n_samples_fit_}\n'
        self.header_str += 'extern char* LABELS[NUM_CLASSES];\n'
        self.header_str += 'extern const float DATA[NUM_SAMPLES][NUM_FEATURES];\n'
        self.header_str += 'extern const int DATA_LABELS[NUM_SAMPLES];\n'
        self.header_str += '#endif'

    def create_source(self):
        super().create_source()
        self.source_str += f'char* labels[NUM_CLASSES] = {np2str(self.clf.classes_)};\n'
        self.source_str += f'const float data[NUM_SAMPLES][NUM_FEATURES] = {np2str(self.clf._fit_X)};\n'
        self.source_str += f'const int DATA_LABELS[NUM_SAMPLES] = {np2str(self.clf._y)};\n'
    

class SVMExporter(GenericExporter):
    def __init__(self, svm_classifier) -> None:
        super().__init__()
        self.clf = svm_classifier
        self.num_classes = len(self.clf.classes_)
        self.num_intercept = self.num_classes * (self.num_classes - 1) // 2
        self.w_sum_arr = np.append([0], np.cumsum(self.clf.n_support_))
    
    def create_header(self):
        super().create_header()
        self.header_str += f'#define NUM_CLASSES {self.num_classes}\n'
        self.header_str += f'#define NUM_INTERCEPTS {self.num_intercept}\n'
        self.header_str += f'#define NUM_FEATURES {self.clf.n_features_in_}\n'
        self.header_str += f'#define NUM_SV {np.sum(self.clf.n_support_)}\n'
        self.header_str += 'enum KernelType{\n\tLINEAR,\n\tPOLY,\n\tRBF\n};\n'
        self.header_str += 'extern const float coeffs[NUM_CLASSES - 1][NUM_SV];\n'
        self.header_str += 'extern const float SV[NUM_SV][NUM_FEATURES];\n'
        self.header_str += 'extern const float intercepts[NUM_INTERCEPTS];\n'
        self.header_str += 'extern const float w_sum[NUM_CLASSES + 1];\n'
        self.header_str += 'extern const float svm_gamma;\n'
        self.header_str += 'extern const float coef0;\n'
        self.header_str += 'extern const int degree;\n'
        self.header_str += 'extern const enum KernelType type;\n'
        self.header_str += '#endif'
    
    def create_source(self):
        super().create_source()
        self.source_str += f'const float coeffs[NUM_CLASSES - 1][NUM_SV] = {np2str(self.clf.dual_coef_)};\n'
        self.source_str += f'const float SV[NUM_SV][NUM_FEATURES] = {np2str(self.clf.support_vectors_)};\n'
        self.source_str += f'const float intercepts[NUM_INTERCEPTS] = {np2str(self.clf.intercept_)};\n'
        self.source_str += f'const float w_sum[NUM_CLASSES + 1] = {np2str(self.w_sum_arr)};\n'
        self.source_str += f'const float svm_gamma = {self.clf._gamma};\n'
        self.source_str += f'const float coef0 = {self.clf.coef0};\n'
        self.source_str += f'const int degree = {self.clf.degree};\n'
        self.source_str += f'const enum KernelType type = {(self.clf.kernel).upper()};\n'

