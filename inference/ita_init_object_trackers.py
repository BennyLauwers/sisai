from deep_sort_realtime.deepsort_tracker import DeepSort

def initialize_object_trackers():    
    object_tracker_person = DeepSort(max_age=30,
                                n_init=3,
                                nms_max_overlap=0.7,
                                max_cosine_distance=0.3,
                                nn_budget=256,
                                override_track_class=None,
                                embedder="mobilenet",
                                half=True,
                                bgr=True,
                                embedder_gpu=False,
                                embedder_model_name=None,
                                embedder_wts=None,
                                polygon=False,
                                today=None)

    object_tracker_car = DeepSort(max_age=30,
                              n_init=3,
                              nms_max_overlap=0.7,
                              max_cosine_distance=0.3,
                              nn_budget=256,
                              override_track_class=None,
                              embedder="mobilenet",
                              half=True,
                              bgr=True,
                              embedder_gpu=False,
                              embedder_model_name=None,
                              embedder_wts=None,
                              polygon=False,
                              today=None)


    object_tracker_truck = DeepSort(max_age=30,
                              n_init=3,
                              nms_max_overlap=0.7,
                              max_cosine_distance=0.3,
                              nn_budget=256,
                              override_track_class=None,
                              embedder="mobilenet",
                              half=True,
                              bgr=True,
                              embedder_gpu=False,
                              embedder_model_name=None,
                              embedder_wts=None,
                              polygon=False,
                              today=None)
    
    return object_tracker_person, object_tracker_car, object_tracker_truck