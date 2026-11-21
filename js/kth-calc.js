// HDB upgrade calculator: what new home budget a "sell first, then buy" upgrade supports.
// Indicative only. Rules used (check before changing):
//  - BSD residential tiers from IRAS (1/2/3/4/5/6%).
//  - LTV 75% on a first housing loan, at least 5% of the price in cash.
//  - TDSR 55% of gross monthly income, tested at a 4% p.a. stress rate (editable).
//  - Loan tenure: up to 30 years for private property, ending by age 65 for the full 75% LTV.
//  - CPF refund on sale = principal used + accrued interest at 2.5% p.a. (estimate, compounded yearly).
(function(){
  const $=id=>document.getElementById(id);
  const form=$('calc-form');if(!form)return;
  const num=id=>{const v=parseFloat(String($(id).value).replace(/[^\d.]/g,''));return isFinite(v)?v:0};
  const fmt=n=>'S$'+Math.round(n).toLocaleString('en-SG');

  function bsd(price){
    const tiers=[[180000,.01],[180000,.02],[640000,.03],[500000,.04],[1500000,.05],[Infinity,.06]];
    let left=price,duty=0;
    for(const [band,rate] of tiers){const part=Math.min(left,band);duty+=part*rate;left-=part;if(left<=0)break}
    return Math.floor(duty);
  }
  function loanFromPayment(pmt,annualRate,years){
    const r=annualRate/12,n=years*12;
    if(pmt<=0||n<=0)return 0;
    return r===0?pmt*n:pmt*(1-Math.pow(1+r,-n))/r;
  }
  function paymentFromLoan(loan,annualRate,years){
    const r=annualRate/12,n=years*12;
    if(loan<=0||n<=0)return 0;
    return r===0?loan/n:loan*r/(1-Math.pow(1+r,-n));
  }

  // Keep money inputs readable with thousands separators.
  form.querySelectorAll('.money input').forEach(inp=>{
    inp.addEventListener('blur',()=>{const v=num(inp.id);inp.value=v?Math.round(v).toLocaleString('en-SG'):''});
  });

  function run(){
    const sale=num('c-sale'),loan=num('c-loan'),cpfUsed=num('c-cpf'),yrs=num('c-years');
    const costsPct=num('c-costs')/100,savings=num('c-cash'),cpfOA=num('c-oa');
    const income=num('c-income'),debts=num('c-debts'),age=num('c-age')||40;
    const stress=(num('c-rate')||4)/100;

    const accrued=cpfUsed*(Math.pow(1.025,yrs)-1);
    const costs=sale*costsPct;
    const refundDue=cpfUsed+accrued;
    const afterLoan=Math.max(0,sale-loan-costs);
    const refund=Math.min(refundDue,afterLoan);          // CPF takes back what the sale can cover
    const cashOut=Math.max(0,afterLoan-refund);

    const cash=cashOut+savings, cpf=refund+cpfOA;
    const tenure=Math.max(0,Math.min(30,65-age));
    const pmtCap=Math.max(0,income*.55-debts);
    const loanCap=tenure>=5?loanFromPayment(pmtCap,stress,tenure):0;

    // Largest price where: cash >= 5% of price, and cash + CPF cover (price - loan + BSD).
    const fits=x=>{const l=Math.min(.75*x,loanCap);return cash>=.05*x&&cash+cpf>=x-l+bsd(x)};
    let lo=0,hi=10000000;
    for(let i=0;i<60;i++){const mid=(lo+hi)/2;if(fits(mid))lo=mid;else hi=mid}
    const budget=Math.floor(lo/1000)*1000;
    const usedLoan=Math.min(.75*budget,loanCap);

    let why;
    if(budget<=0)why='Add your income and sale figures to see a budget.';
    else if(usedLoan<.75*budget-1)why='Your income (the 55% TDSR limit) caps the loan, so the loan, not your cash, sets this budget.';
    else if(cash<.05*budget+1000)why='Your cash sets this budget: at least 5% of the price has to be paid in cash.';
    else why='Your cash and CPF for the 25% downpayment and stamp duty set this budget. The loan has room to spare.';

    $('o-sale').textContent=fmt(sale);
    $('o-loan').textContent='− '+fmt(loan);
    $('o-costs').textContent='− '+fmt(costs);
    $('o-refund').textContent='− '+fmt(refund);
    $('o-cashout').textContent=fmt(cashOut);
    $('o-cash').textContent=fmt(cash);
    $('o-cpf').textContent=fmt(cpf);
    $('o-loancap').textContent=fmt(loanCap);
    $('o-tenure').textContent=tenure+' yrs';
    const out=$('o-budget');
    out.textContent=budget>0?fmt(budget):'S$0';
    out.classList.add('tick');setTimeout(()=>out.classList.remove('tick'),300);
    $('o-why').textContent=why;
    const bar=$('o-bar');if(bar)bar.textContent=out.textContent;
    $('o-bsd').textContent=fmt(bsd(budget));
    $('o-pmt').textContent=fmt(paymentFromLoan(usedLoan,stress,tenure||1))+'/mth';

    const warn=$('o-warn');
    if(sale>0&&refund<refundDue-1){warn.hidden=false;warn.textContent='Your sale may not cover the full CPF refund plus interest. This is called a negative sale on the CPF side. Talk it through with me before you list.'}
    else if(tenure<5){warn.hidden=false;warn.textContent='At this age a bank may offer a shorter tenure or a lower loan. I can work through the options with you.'}
    else warn.hidden=true;

    const snap=`Sale ${fmt(sale)}, loan ${fmt(loan)}, CPF used ${fmt(cpfUsed)} (${yrs} yrs), cash ${fmt(savings)}, CPF OA ${fmt(cpfOA)}, income ${fmt(income)}/mth, debts ${fmt(debts)}/mth, age ${age} → est. cash from sale ${fmt(cashOut)}, budget ${fmt(budget)}`;
    $('c-snapshot').value=snap;
    $('o-wa').href='https://wa.me/'+(window.KTH_WHATSAPP||'6581668767')+'?text='+encodeURIComponent('Hi Louis, I used your HDB upgrade calculator. Could you check my numbers?\n'+snap);
  }
  form.addEventListener('input',run);
  run();
})();
