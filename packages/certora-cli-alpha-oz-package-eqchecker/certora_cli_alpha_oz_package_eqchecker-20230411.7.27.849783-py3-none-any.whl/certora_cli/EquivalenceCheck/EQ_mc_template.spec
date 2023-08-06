using CONTRACTB as B

// sets everything but the callee the same in two environments
function e_equivalence(env e1, env e2) {
    require e1.msg.sender == e2.msg.sender;
    require e1.block.timestamp == e2.block.timestamp;
    require e1.msg.value == e2.msg.value;
    // require e1.msg.data == e2.msg.data;
}

rule equivalence_of_revert_conditions() 
{
    bool <Fa>_revert;
    bool <Fb>_revert;
    // using this opposed to generating input parameters is experimental
    env e_<Fa>; calldataarg args;
    env e_<Fb>;
    e_equivalence(e_<Fa>, e_<Fb>);

    <Fa>@withrevert(e_<Fa>, args);
    <Fa>_revert = lastReverted;

    B.<Fb>@withrevert(e_<Fb>, args);
    <Fb>_revert = lastReverted;

    assert(<Fa>_revert == <Fb>_revert);
}

rule equivalence_of_return_value() 
{  
    OUTPUTS_DEC

    env e_<Fa>; calldataarg args;
    env e_<Fb>;

    e_equivalence(e_<Fa>, e_<Fb>);

    OUTPUTS_IN_A = <Fa>(e_<Fa>, args);
    OUTPUTS_IN_B = B.<Fb>(e_<Fb>, args);

    COMPARE_OUTPUTS
}