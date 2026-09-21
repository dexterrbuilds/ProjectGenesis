/** Maintainer tool: explicit fixture-only catalog generation, never invoked by install/boot. */
import {writeFileSync} from 'node:fs';
import {deploymentFixture} from '../tests/support/deployment-fixture.ts';
import {catalog,source} from '../runtime/deployment/schema.ts';
await deploymentFixture(async pool=>{
 const c=await pool.connect();try{
 writeFileSync('runtime/deployment/catalog-baseline.json',JSON.stringify(await catalog(c),null,2)+'\n');
 for(const path of ['runtime/preparation-schema.sql','runtime/one-shot-schema.sql','runtime/continuous-schema.sql','runtime/operator-schema-v1.sql','runtime/provider-integration-schema.sql','runtime/deployment/release.sql'])await c.query(source(path));
 writeFileSync('runtime/deployment/catalog-installed.json',JSON.stringify(await catalog(c),null,2)+'\n');
 }finally{c.release();}
});
