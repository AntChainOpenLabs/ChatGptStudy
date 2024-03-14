from openai import OpenAI
client = OpenAI()
#jobs_obj = client.fine_tuning.jobs.list(limit=20)
#print(jobs_obj)
completion = client.chat.completions.create(
  model="ft:gpt-3.5-turbo-0125:antchainopenlab::8zPANCCT",
  messages=[
    {"role": "system", "content": "You're a smart contract vulnerability identification assistant."},
    {"role": "user", "content": "pragma solidity ^0.8.17;\ncontract Pair is ERC20, ERC721TokenReceiver {\n using SafeTransferLib for address;\n using SafeTransferLib for ERC20;\n\n uint256 public constant ONE = 1e18;\n uint256 public constant CLOSE_GRACE_PERIOD = 7 days;\n\n address public immutable nft;\n address public immutable baseToken; \/\/ address(0) for ETH\n bytes32 public immutable merkleRoot;\n LpToken public immutable lpToken;\n Caviar public immutable caviar;\n uint256 public closeTimestamp;\n\n event Add(uint256 baseTokenAmount, uint256 fractionalTokenAmount, uint256 lpTokenAmount);\n event Remove(uint256 baseTokenAmount, uint256 fractionalTokenAmount, uint256 lpTokenAmount);\n event Buy(uint256 inputAmount, uint256 outputAmount);\n event Sell(uint256 inputAmount, uint256 outputAmount);\n event Wrap(uint256[] tokenIds);\n event Unwrap(uint256[] tokenIds);\n event Close(uint256 closeTimestamp);\n event Withdraw(uint256 tokenId);\n\n constructor(\n  address _nft,\n  address _baseToken,\n  bytes32 _merkleRoot,\n  string memory pairSymbol,\n  string memory nftName,\n  string memory nftSymbol\n ) ERC20(string.concat(nftName, \" fractional token\"), string.concat(\"f\", nftSymbol), 18) {\n  nft = _nft;\n  baseToken = _baseToken;\n  merkleRoot = _merkleRoot;\n  lpToken = new LpToken(pairSymbol);\n  caviar = Caviar(msg.sender);\n }\n function add(uint256 baseTokenAmount, uint256 fractionalTokenAmount, uint256 minLpTokenAmount)\n  public\n  payable\n  returns (uint256 lpTokenAmount)\n {\n  require(baseTokenAmount > 0 && fractionalTokenAmount > 0, \"Input token amount is zero\");\n  require(baseToken == address(0) ? msg.value == baseTokenAmount : msg.value == 0, \"Invalid ether input\");\n  lpTokenAmount = addQuote(baseTokenAmount, fractionalTokenAmount);\n  require(lpTokenAmount >= minLpTokenAmount, \"Slippage: lp token amount out\");\n  _transferFrom(msg.sender, address(this), fractionalTokenAmount);\n  lpToken.mint(msg.sender, lpTokenAmount);\n  if (baseToken != address(0)) {\nERC20(baseToken).safeTransferFrom(msg.sender, address(this), baseTokenAmount);\n  }\n  emit Add(baseTokenAmount, fractionalTokenAmount, lpTokenAmount);\n }\n function buy(uint256 outputAmount, uint256 maxInputAmount) public payable returns (uint256 inputAmount) {\n  require(baseToken == address(0) ? msg.value == maxInputAmount : msg.value == 0, \"Invalid ether input\");\n  inputAmount = buyQuote(outputAmount);\n  require(inputAmount <= maxInputAmount, \"Slippage: amount in\");\n  _transferFrom(address(this), msg.sender, outputAmount);\n  if (baseToken == address(0)) {\nuint256 refundAmount = maxInputAmount - inputAmount;\nif (refundAmount > 0) msg.sender.safeTransferETH(refundAmount);\n  } else {\nERC20(baseToken).safeTransferFrom(msg.sender, address(this), inputAmount);\n  }\n  emit Buy(inputAmount, outputAmount);\n }\n function nftSell(uint256[] calldata tokenIds, uint256 minOutputAmount, bytes32[][] calldata proofs)\n  public\n  returns (uint256 outputAmount)\n {\n  uint256 inputAmount = wrap(tokenIds, proofs);\n  outputAmount = sell(inputAmount, minOutputAmount);\n }\n function baseTokenReserves() public view returns (uint256) {\n  return _baseTokenReserves();\n }\n\n function fractionalTokenReserves() public view returns (uint256) {\n  return balanceOf[address(this)];\n }\n\n function buyQuote(uint256 outputAmount) public view returns (uint256) {\n  return (outputAmount * 1000 * baseTokenReserves()) \/ ((fractionalTokenReserves() - outputAmount) * 997);\n }\n\n\n function sellQuote(uint256 inputAmount) public view returns (uint256) {\n  uint256 inputAmountWithFee = inputAmount * 997;\n  return (inputAmountWithFee * baseTokenReserves()) \/ ((fractionalTokenReserves() * 1000) + inputAmountWithFee);\n }\n\n function addQuote(uint256 baseTokenAmount, uint256 fractionalTokenAmount) public view returns (uint256) {\n  uint256 lpTokenSupply = lpToken.totalSupply();\n  if (lpTokenSupply > 0) {\nuint256 baseTokenShare = (baseTokenAmount * lpTokenSupply) \/ baseTokenReserves();\nuint256 fractionalTokenShare = (fractionalTokenAmount * lpTokenSupply) \/ fractionalTokenReserves();\nreturn Math.min(baseTokenShare, fractionalTokenShare);\n  } else {\nreturn Math.sqrt(baseTokenAmount * fractionalTokenAmount);\n  }\n }\n function removeQuote(uint256 lpTokenAmount) public view returns (uint256, uint256) {\n  uint256 lpTokenSupply = lpToken.totalSupply();\n  uint256 baseTokenOutputAmount = (baseTokenReserves() * lpTokenAmount) \/ lpTokenSupply;\n  uint256 fractionalTokenOutputAmount = (fractionalTokenReserves() * lpTokenAmount) \/ lpTokenSupply;\n\n  return (baseTokenOutputAmount, fractionalTokenOutputAmount);\n }\n\n}\n\n###\n\n"}
  ]
)
print(completion.choices[0].message.content)