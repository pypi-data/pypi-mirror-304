import collections
import unittest
import torch
from irisml.tasks.sample_few_shot_dataset import Task

from utils import FakeDatasetWithGetTargets


class TestSampleFewShotDataset(unittest.TestCase):
    def test_ic_multiclass_few_shot(self):
        dataset = [(None, torch.tensor(i % 10)) for i in range(100)]
        for i in range(10):
            outputs = Task(Task.Config(1, random_seed=i)).execute(Task.Inputs(dataset))
            self.assertGreaterEqual(len(outputs.dataset), 10)
            classes = set(int(t) for _, t in outputs.dataset)
            self.assertEqual(len(classes), 10)

    def test_ic_multiclass_few_shot_rare_classes(self):
        """Test some classes have less than n_shot images."""
        dataset = [(None, torch.tensor(c)) for c in [0, 1, 1, 1, 2, 2, 2, 2]]
        for i in range(10):
            outputs = Task(Task.Config(n_shot=2, random_seed=i, strict=False)).execute(Task.Inputs(dataset))
            # Can only sample 1 image for class 0, and 2 for class 1,2
            self.assertEqual(len(outputs.dataset), 5)
            classes = set(int(t) for _, t in outputs.dataset)
            self.assertEqual(len(classes), 3)

    def test_default_seed(self):
        dataset = [(None, torch.tensor(i % 10)) for i in range(100)]
        all_classes = []
        for i in range(10):
            outputs = Task(Task.Config(1)).execute(Task.Inputs(dataset))
            classes = [int(t) for _, t in outputs.dataset]
            all_classes.append(classes)
            if i > 0:
                self.assertEqual(classes, all_classes[0])

    def test_od_few_shot(self):
        dataset = [(None, torch.tensor([[0, 0, 0, 0.5, 0.5], [1, 0.5, 0.5, 1, 1]])), (None, torch.tensor([[1, 0, 0, 0.2, 0.2], [1, 0.2, 0.2, 0.4, 0.4]])), (None, torch.tensor([[0, 0, 0, 1, 1]]))]
        outputs = Task(Task.Config(2)).execute(Task.Inputs(dataset))
        self.assertEqual(len(outputs.dataset), 3)

        classes_counter = collections.Counter()
        for _, targets in dataset:
            classes_counter.update(set(int(t[0]) for t in targets))

        for n_images in classes_counter.values():
            self.assertGreaterEqual(n_images, 2)

        dataset = [(None, torch.tensor([[0, 0, 0, 0.5, 0.5], [1, 0.5, 0.5, 1, 1]])),
                   (None, torch.tensor([[0, 0, 0, 0.2, 0.2]])), (None, torch.tensor([[0, 0, 0, 1, 1]])), (None, torch.tensor([[0, 0, 0, 1, 1]]))]
        outputs = Task(Task.Config(1)).execute(Task.Inputs(FakeDatasetWithGetTargets(dataset)))
        self.assertLessEqual(len(outputs.dataset), 2)

    def test_ic_multiclass_get_targets(self):
        dataset = FakeDatasetWithGetTargets([(None, torch.tensor([1])), (None, torch.tensor([1])), (None, torch.tensor([0]))])
        outputs = Task(Task.Config(1)).execute(Task.Inputs(dataset))
        self.assertGreaterEqual(len(outputs.dataset), 2)
