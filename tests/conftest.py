"""
pytest 配置和共享 fixtures
"""

import os
import pytest
from unittest.mock import Mock, patch


@pytest.fixture(autouse=True)
def mock_model_loading():
    """在 CI 环境中自动 mock 模型加载"""
    if os.getenv("SKIP_MODEL_LOAD", "false").lower() == "true":
        with patch("engine.models.AutoModelForCausalLM.from_pretrained") as mock_model, \
             patch("engine.models.AutoTokenizer.from_pretrained") as mock_tokenizer:
            # 创建 mock tokenizer
            mock_tok = Mock()
            mock_tok.pad_token = None
            mock_tok.eos_token = "<|eot_id|>"
            mock_tok.pad_token_id = 0
            mock_tok.eos_token_id = 128001
            mock_tokenizer.return_value = mock_tok
            
            # 创建 mock model
            mock_mod = Mock()
            mock_mod.eval.return_value = None
            mock_mod.parameters.return_value = [Mock(device=Mock())]
            mock_model.return_value = mock_mod
            
            yield
    else:
        yield


@pytest.fixture
def mock_model_manager():
    """提供 mock 的 ModelManager，避免加载真实模型"""
    from engine.models import ModelManager
    
    with patch.object(ModelManager, "load_llm"), \
         patch.object(ModelManager, "load_guard"), \
         patch.object(ModelManager, "generate"), \
         patch.object(ModelManager, "moderate"):
        manager = ModelManager()
        yield manager

