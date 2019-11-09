from tf_keras.finetune.imports import *
from system.imports import *

from tf_keras.finetune.level_5_state_base import finetune_state

class prototype_params(finetune_state):
    @accepts("self", verbose=int, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def __init__(self, verbose=1):
        super().__init__(verbose=verbose);


    ###############################################################################################################################################
    @warning_checks(None, dataset_path=None, path_to_csv=None, delimiter=None,
        split=["gt", 0.5], input_size=["gte", 32, "lte", 1024], batch_size=["lte", 128], shuffle_data=None, num_processors=["lte", psutil.cpu_count()], post_trace=True)
    @error_checks(None, dataset_path=["folder", "r"], path_to_csv=["file", "r"], delimiter=["in", [",", ";", "-", " "]],
        split=["gt", 0.0, "lt", 1.0], input_size=["gt", 0], batch_size=["gt", 0], shuffle_data=None, num_processors=["gt", 0],  post_trace=True)
    @accepts("self", dataset_path=[str, list, bool], path_to_csv=[str, list, bool], delimiter=str, split=float, 
        input_size=int, batch_size=int, shuffle_data=bool, num_processors=int, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Dataset_Params(self, dataset_path=False, path_to_csv=False, delimiter=",", split=0.9,
        input_size=224, batch_size=16, shuffle_data=True, num_processors=psutil.cpu_count()):
        if(self.system_dict["states"]["eval_infer"]):
            if(not self.system_dict["dataset"]["params"]["input_size"]):
                self.system_dict = set_input_size(input_size, self.system_dict);
            if(not self.system_dict["dataset"]["params"]["num_workers"]):
                self.system_dict = set_num_processors(num_processors, self.system_dict);
            self.system_dict = set_dataset_test_path(self.system_dict, dataset_path, path_to_csv, delimiter);
            self.custom_print("Dataset Details");
            self.custom_print("    Test path:     {}".format(self.system_dict["dataset"]["test_path"]));
            self.custom_print("    CSV test path:  {}".format(self.system_dict["dataset"]["csv_test"]));
            self.custom_print("");

            self.custom_print("Dataset Params");
            self.custom_print("    Input Size:  {}".format(self.system_dict["dataset"]["params"]["input_size"]));
            self.custom_print("    Processors:   {}".format(self.system_dict["dataset"]["params"]["num_workers"]));
            if("csv" in self.system_dict["dataset"]["params"]["dataset_test_type"]):
                self.custom_print("    Delimiter:   {}".format(self.system_dict["dataset"]["params"]["test_delimiter"]));
            self.custom_print("");

        else:
            self.system_dict = set_input_size(input_size, self.system_dict);
            self.system_dict = set_batch_size(batch_size, self.system_dict);
            self.system_dict = set_data_shuffle(shuffle_data, self.system_dict);
            self.system_dict = set_num_processors(num_processors, self.system_dict);
            self.system_dict = set_dataset_train_path(self.system_dict, dataset_path, split, path_to_csv, delimiter);

            self.custom_print("Dataset Details");
            self.custom_print("    Train path:     {}".format(self.system_dict["dataset"]["train_path"]));
            self.custom_print("    Val path:       {}".format(self.system_dict["dataset"]["val_path"]));
            self.custom_print("    CSV train path: {}".format(self.system_dict["dataset"]["csv_train"]));
            self.custom_print("    CSV val path:  {}".format(self.system_dict["dataset"]["csv_val"]));
            self.custom_print("");


            self.custom_print("Dataset Params");
            self.custom_print("    Input Size:  {}".format(self.system_dict["dataset"]["params"]["input_size"]));
            self.custom_print("    Batch Size:  {}".format(self.system_dict["dataset"]["params"]["batch_size"]));
            self.custom_print("    Data Shuffle: {}".format(self.system_dict["dataset"]["params"]["train_shuffle"]));
            self.custom_print("    Processors:   {}".format(self.system_dict["dataset"]["params"]["num_workers"]));
            if("val" not in self.system_dict["dataset"]["dataset_type"]):
                self.custom_print("    Train-val split:   {}".format(self.system_dict["dataset"]["params"]["train_val_split"]));
            if("csv" in self.system_dict["dataset"]["dataset_type"]):
                self.custom_print("    Delimiter:   {}".format(self.system_dict["dataset"]["params"]["delimiter"]));
            self.custom_print("");
    ###############################################################################################################################################




    ###############################################################################################################################################
    @error_checks(None, model_name=None, freeze_base_network=None, use_gpu=None, gpu_memory_fraction=["gt", 0, "lt", 1],  
        use_pretrained=None, model_path=["file", 'r'], post_trace=True)
    @accepts("self", model_name=str, freeze_base_network=bool, use_gpu=bool, gpu_memory_fraction=float, use_pretrained=bool, model_path=[bool, str, list],  post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Model_Params(self, model_name="resnet50", freeze_base_network=True, use_gpu=True, gpu_memory_fraction=0.5, use_pretrained=True, model_path=False):
        if(self.system_dict["states"]["copy_from"]):
            msg = "Cannot set model params in Copy-From mode.\n";
            raise ConstraintError(msg)


        if(model_path):
            self.system_dict = set_model_path(model_path, self.system_dict)
        else:
            self.system_dict = set_model_name(model_name, self.system_dict);
            self.system_dict = set_pretrained(use_pretrained, self.system_dict);
        if(use_gpu):
            self.system_dict = set_gpu_memory_fraction(gpu_memory_fraction, self.system_dict);
        self.system_dict = set_device(use_gpu, self.system_dict);
        self.system_dict = set_freeze_base_network(freeze_base_network, self.system_dict);


        self.custom_print("Model Params");
        self.custom_print("    Model name:           {}".format(self.system_dict["model"]["params"]["model_name"]));
        self.custom_print("    Use Gpu:              {}".format(self.system_dict["model"]["params"]["use_gpu"]));
        if(use_gpu):
            self.custom_print("    Gpu Memory Fraction:  {}".format(self.system_dict["model"]["params"]["gpu_memory_fraction"]));
        self.custom_print("    Use pretrained:       {}".format(self.system_dict["model"]["params"]["use_pretrained"]));
        self.custom_print("    Freeze base network:  {}".format(self.system_dict["model"]["params"]["freeze_base_network"]));
        self.custom_print("");
    ###############################################################################################################################################



    ###############################################################################################################################################
    @warning_checks(None, num_epochs=["lt", 100], display_progress=None, display_progress_realtime=None,
        save_intermediate_models=None, intermediate_model_prefix=None, save_training_logs=None, post_trace=True)
    @error_checks(None, num_epochs=["gt", 0], display_progress=None, display_progress_realtime=None,
        save_intermediate_models=None, intermediate_model_prefix=["name", ["A-Z", "a-z", "0-9", "-", "_"]], save_training_logs=False, post_trace=True)
    @accepts("self", num_epochs=int, display_progress=bool, display_progress_realtime=bool, 
        save_intermediate_models=bool, intermediate_model_prefix=str, save_training_logs=bool, post_trace=True)
    @TraceFunction(trace_args=True, trace_rv=True)
    def Training_Params(self, num_epochs=10, display_progress=True, display_progress_realtime=True, 
        save_intermediate_models=True, intermediate_model_prefix="intermediate_model_", save_training_logs=True):

        if(save_intermediate_models):
            if(not os.access(self.system_dict["model_dir"], os.W_OK)):
                msg = "Folder \"{}\" has no read access".format(self.system_dict["model_dir"])
                msg += "Cannot save Intermediate models";
                raise ConstraintError(msg);

        self.system_dict = set_num_epochs(num_epochs, self.system_dict);
        self.system_dict = set_display_progress_realtime(display_progress_realtime, self.system_dict);
        self.system_dict = set_display_progress(display_progress, self.system_dict);
        self.system_dict = set_save_intermediate_models(save_intermediate_models, self.system_dict);
        self.system_dict = set_save_training_logs(save_training_logs, self.system_dict);
        self.system_dict = set_intermediate_model_prefix(intermediate_model_prefix, self.system_dict);

        self.custom_print("Training params");
        self.custom_print("    Num Epochs: {}".format(self.system_dict["hyper-parameters"]["num_epochs"]));
        self.custom_print("");

        self.custom_print("Display params");
        self.custom_print("    Display progress:          {}".format(self.system_dict["training"]["settings"]["display_progress"]));
        self.custom_print("    Display progress realtime: {}".format(self.system_dict["training"]["settings"]["display_progress_realtime"]));
        self.custom_print("    Save Training logs:        {}".format(self.system_dict["training"]["settings"]["save_training_logs"]));
        self.custom_print("    Save Intermediate models:  {}".format(self.system_dict["training"]["settings"]["save_intermediate_models"]));
        if(self.system_dict["training"]["settings"]["save_intermediate_models"]):
            self.custom_print("    Intermediate model prefix: {}".format(self.system_dict["training"]["settings"]["intermediate_model_prefix"]));
        self.custom_print("");
    ###############################################################################################################################################